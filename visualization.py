from pyvis.network import Network
from pathlib import Path
import json

# Reuse your teammates' Python implementations.
from Algorithms import bfs, dfs, shortest_path, degrees_of_separation
from analysis import (
    mutual_friends,
    recommend_friends,
    most_connected_users,
    network_statistics,
    connected_components
)


class _NetworkAdapter:
    """Allows analysis.py functions to work when a plain dictionary is supplied."""

    def __init__(self, graph):
        self.graph = graph

    def get_friendship_count(self):
        return sum(len(friends) for friends in self.graph.values()) // 2


def create_visualization(
    graph,
    shortest_path=None,
    output_path="static/social_network.html"
):
    """
    Create an interactive Social Network Analyzer dashboard.

    `graph` can be either:
      - a SocialNetwork object from graph.py, or
      - its adjacency dictionary.

    The dashboard includes BFS, DFS, shortest path, degrees of separation,
    mutual friends, friend recommendations, most-connected users,
    connected components, network statistics, and sorting controls.
    """

    # Accept either a SocialNetwork object or its dictionary.
    network_object = graph if hasattr(graph, "graph") else _NetworkAdapter(graph)
    graph_data = network_object.graph

    # Make a clean JSON-compatible adjacency list.
    adjacency = {
        str(user): sorted(str(friend) for friend in friends)
        for user, friends in graph_data.items()
    }

    # Prepare output directory.
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # Run the existing Python algorithms for initial analysis.
    users = sorted(graph_data, key=lambda value: str(value))
    initial_user = users[0] if users else None

    initial_analysis = {
        "statistics": network_statistics(network_object),
        "most_connected": most_connected_users(network_object),
        "components": [
            sorted(str(user) for user in component)
            for component in connected_components(network_object)
        ],
        "bfs": bfs(network_object, initial_user) if initial_user is not None else [],
        "dfs": dfs(network_object, initial_user) if initial_user is not None else [],
        "recommendations": (
            recommend_friends(network_object, initial_user)
            if initial_user is not None else []
        )
    }

    # Convert sets / dictionaries into JSON-friendly values.
    initial_analysis["statistics"]["friends_per_user"] = {
        str(user): count
        for user, count in
        initial_analysis["statistics"]["friends_per_user"].items()
    }
    initial_analysis["statistics"]["users_without_friends"] = [
        str(user)
        for user in initial_analysis["statistics"]["users_without_friends"]
    ]
    initial_analysis["most_connected"] = [
        str(user) for user in initial_analysis["most_connected"]
    ]
    initial_analysis["bfs"] = [str(user) for user in initial_analysis["bfs"]]
    initial_analysis["dfs"] = [str(user) for user in initial_analysis["dfs"]]
    initial_analysis["recommendations"] = [
        [str(user), count]
        for user, count in initial_analysis["recommendations"]
    ]

    # Create the interactive PyVis graph.
    net = Network(
        height="calc(100vh - 100px)",
        width="100%",
        bgcolor="#081120",
        font_color="#eaf2ff",
        directed=False,
        notebook=False,
        cdn_resources="in_line"
    )

    # Optional path supplied by the caller.
    path_nodes = set(shortest_path) if shortest_path else set()
    path_edges = set()

    if shortest_path:
        for index in range(len(shortest_path) - 1):
            path_edges.add(
                frozenset((
                    str(shortest_path[index]),
                    str(shortest_path[index + 1])
                ))
            )

    # Add nodes with actual usernames / dataset IDs as labels.
    for username, friends in adjacency.items():
        degree = len(friends)

        if username in {str(user) for user in path_nodes}:
            node_color = {
                "background": "#22c55e",
                "border": "#bbf7d0",
                "highlight": {
                    "background": "#4ade80",
                    "border": "#ffffff"
                }
            }
        else:
            node_color = {
                "background": "#168cf0",
                "border": "#8bd5ff",
                "highlight": {
                    "background": "#6366f1",
                    "border": "#ffffff"
                },
                "hover": {
                    "background": "#38bdf8",
                    "border": "#ffffff"
                }
            }

        net.add_node(
            username,
            label=username,
            title=f"User: {username}<br>Friends: {degree}",
            size=18 + min(degree, 15),
            shape="dot",
            color=node_color,
            borderWidth=2,
            font={
                "size": 17,
                "color": "#f8fafc",
                "face": "Arial",
                "strokeWidth": 3,
                "strokeColor": "#081120"
            }
        )

    # Add each undirected friendship only once.
    added_edges = set()

    for username, friends in adjacency.items():
        for friend in friends:
            edge_key = frozenset((username, friend))

            if edge_key in added_edges:
                continue

            added_edges.add(edge_key)

            if edge_key in path_edges:
                net.add_edge(
                    username,
                    friend,
                    color="#22c55e",
                    width=5,
                    title="Shortest-path connection"
                )
            else:
                net.add_edge(
                    username,
                    friend,
                    color={
                        "color": "#344765",
                        "highlight": "#a78bfa",
                        "hover": "#60a5fa"
                    },
                    width=1.4,
                    title=f"{username} ↔ {friend}"
                )

    # Graph layout and interaction settings.
    options = {
        "nodes": {
            "scaling": {"min": 18, "max": 34}
        },
        "edges": {
            "smooth": {"type": "continuous"},
            "selectionWidth": 3,
            "hoverWidth": 2
        },
        "interaction": {
            "hover": True,
            "tooltipDelay": 120,
            "navigationButtons": True,
            "keyboard": True,
            "multiselect": True
        },
        "physics": {
            "enabled": True,
            "solver": "forceAtlas2Based",
            "forceAtlas2Based": {
                "gravitationalConstant": -55,
                "centralGravity": 0.012,
                "springLength": 125,
                "springConstant": 0.08,
                "damping": 0.42,
                "avoidOverlap": 0.8
            },
            "minVelocity": 0.75,
            "stabilization": {
                "enabled": True,
                "iterations": 180
            }
        }
    }
    net.set_options(json.dumps(options))

    # Generate the PyVis HTML first.
    net.write_html(str(output_file))
    html = output_file.read_text(encoding="utf-8")

    # Safely embed the graph data in JavaScript.
    graph_json = json.dumps(adjacency).replace("</", "<\\/")
    analysis_json = json.dumps(initial_analysis).replace("</", "<\\/")

    dashboard_html = r"""
    <style>
        * { box-sizing: border-box; }

        body {
            margin: 0 !important;
            background: #081120 !important;
            color: #edf4ff;
            font-family: Arial, Helvetica, sans-serif;
            overflow: hidden;
        }

        .sn-header {
            height: 82px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 25px;
            background: linear-gradient(110deg, #0c1830, #172554 65%, #25165a);
            border-bottom: 1px solid #24385d;
        }

        .sn-brand h1 {
            margin: 0;
            font-size: 25px;
            letter-spacing: .2px;
        }

        .sn-brand h1 span { color: #a78bfa; }

        .sn-brand p {
            margin: 6px 0 0;
            color: #9fb4d5;
            font-size: 13px;
        }

        .sn-status {
            color: #9fb4d5;
            font-size: 12px;
        }

        .card {
            position: fixed !important;
            top: 82px !important;
            left: 0 !important;
            width: calc(100% - 350px) !important;
            height: calc(100vh - 82px) !important;
            margin: 0 !important;
            padding: 0 !important;
            border: 0 !important;
            background: transparent !important;
        }

        .card-body {
            height: 100% !important;
            padding: 0 !important;
        }

        #mynetwork {
            width: 100% !important;
            height: 100% !important;
            border: 0 !important;
            background: radial-gradient(circle at 48% 45%, #101f3d, #081120 72%) !important;
        }

        .sn-panel {
            position: fixed;
            top: 82px;
            right: 0;
            bottom: 0;
            width: 350px;
            overflow-y: auto;
            padding: 15px;
            background: #0c172b;
            border-left: 1px solid #263957;
        }

        .sn-card {
            background: linear-gradient(145deg, #111f37, #0d192d);
            border: 1px solid #263957;
            border-radius: 13px;
            padding: 14px;
            margin-bottom: 12px;
            box-shadow: 0 8px 25px rgba(0,0,0,.15);
        }

        .sn-card h3 {
            margin: 0 0 12px;
            font-size: 14px;
            color: #dce9ff;
            letter-spacing: .3px;
        }

        .sn-field-label {
            display: block;
            color: #9fb4d5;
            font-size: 11px;
            margin: 9px 0 5px;
        }

        .sn-panel select, .sn-panel button {
            width: 100%;
            border-radius: 8px;
            padding: 10px;
            border: 1px solid #344b70;
            background: #101f38;
            color: #edf4ff;
            font-size: 12px;
            outline: none;
        }

        .sn-panel button {
            margin-top: 10px;
            cursor: pointer;
            font-weight: 700;
            border: 0;
            background: linear-gradient(100deg, #4f46e5, #7c3aed);
        }

        .sn-panel button:hover { filter: brightness(1.15); }

        .sn-panel button.secondary {
            background: #1c3151;
            border: 1px solid #3b5278;
        }

        .sn-result {
            color: #c8d8f2;
            font-size: 12px;
            line-height: 1.65;
            overflow-wrap: anywhere;
            max-height: 220px;
            overflow-y: auto;
        }

        .sn-stats {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 8px;
        }

        .sn-stat {
            background: #101f38;
            border: 1px solid #263957;
            border-radius: 9px;
            padding: 10px;
        }

        .sn-stat strong {
            display: block;
            color: #60a5fa;
            font-size: 20px;
        }

        .sn-stat span {
            color: #9fb4d5;
            font-size: 10px;
        }

        .sn-legend {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            color: #a9bddb;
            font-size: 10px;
        }

        .sn-dot {
            display: inline-block;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            margin-right: 5px;
        }

        @media (max-width: 850px) {
            body { overflow: auto; }
            .card {
                position: relative !important;
                top: auto !important;
                left: auto !important;
                width: 100% !important;
                height: 60vh !important;
                margin-top: 0 !important;
            }
            .sn-panel {
                position: relative;
                top: auto;
                right: auto;
                bottom: auto;
                width: 100%;
                max-height: none;
            }
            .sn-header { padding: 0 14px; }
            .sn-brand h1 { font-size: 19px; }
            .sn-status { display: none; }
        }
    </style>

    <header class="sn-header">
        <div class="sn-brand">
            <h1>Social Network <span>Analyzer</span></h1>
            <p>Explore connections. Analyze communities. Discover relationships.</p>
        </div>
        <div class="sn-status">INTERACTIVE NETWORK DASHBOARD</div>
    </header>

    <aside class="sn-panel">
            <section class="sn-card">
                <h3>GRAPH ALGORITHMS</h3>

                <label class="sn-field-label" for="algorithm">Choose algorithm</label>
                <select id="algorithm">
                    <option value="bfs">Breadth-First Search (BFS)</option>
                    <option value="dfs">Depth-First Search (DFS)</option>
                    <option value="shortest">Shortest Path</option>
                    <option value="degrees">Degrees of Separation</option>
                    <option value="mutual">Mutual Friends</option>
                    <option value="recommend">Friend Recommendations</option>
                    <option value="connected">Most Connected Users</option>
                    <option value="components">Connected Components</option>
                    <option value="statistics">Network Statistics</option>
                </select>

                <label class="sn-field-label" for="startUser">Starting / first user</label>
                <select id="startUser"></select>

                <label class="sn-field-label" for="endUser">Destination / second user</label>
                <select id="endUser"></select>

                <button onclick="runAlgorithm()">Run Algorithm</button>
                <button class="secondary" onclick="resetGraph()">Reset Graph</button>
            </section>

            <section class="sn-card">
                <h3>SORT USERS</h3>
                <select id="sortMode" onchange="sortUsers()">
                    <option value="degree_desc">Most friends first</option>
                    <option value="degree_asc">Fewest friends first</option>
                    <option value="name_asc">Username A–Z</option>
                    <option value="name_desc">Username Z–A</option>
                </select>
                <div id="sortResult" class="sn-result" style="margin-top:10px">
                    Choose a sorting method.
                </div>
            </section>

            <section class="sn-card">
                <h3>NETWORK OVERVIEW</h3>
                <div class="sn-stats" id="stats"></div>
            </section>

            <section class="sn-card">
                <h3>RESULT</h3>
                <div id="result" class="sn-result">
                    Select an algorithm and press Run Algorithm.
                </div>
            </section>

            <section class="sn-card">
                <h3>LEGEND</h3>
                <div class="sn-legend">
                    <span><i class="sn-dot" style="background:#168cf0"></i>Other users</span>
                    <span><i class="sn-dot" style="background:#22c55e"></i>Selected path / traversal</span>
                    <span><i class="sn-dot" style="background:#f97316"></i>Destination</span>
                </div>
            </section>
    </aside>
    """

    script = r"""
    <script>
        const graphData = __GRAPH_DATA__;
        const initialAnalysis = __ANALYSIS_DATA__;
        const userNames = Object.keys(graphData).sort();

        const startSelect = document.getElementById("startUser");
        const endSelect = document.getElementById("endUser");

        function fillUserSelect(select) {
            select.innerHTML = "";
            userNames.forEach(user => {
                const option = document.createElement("option");
                option.value = user;
                option.textContent = user;
                select.appendChild(option);
            });
        }

        fillUserSelect(startSelect);
        fillUserSelect(endSelect);

        if (userNames.length > 1) endSelect.selectedIndex = 1;

        const stats = initialAnalysis.statistics;
        document.getElementById("stats").innerHTML = `
            <div class="sn-stat"><strong>${stats.total_users}</strong><span>TOTAL USERS</span></div>
            <div class="sn-stat"><strong>${stats.total_friendships}</strong><span>FRIENDSHIPS</span></div>
            <div class="sn-stat"><strong>${Number(stats.average_friends).toFixed(2)}</strong><span>AVERAGE DEGREE</span></div>
            <div class="sn-stat"><strong>${initialAnalysis.components.length}</strong><span>COMMUNITIES</span></div>
        `;

        function showResult(title, content) {
            document.getElementById("result").innerHTML =
                `<b style="color:#a5b4fc">${title}</b><br>${content}`;
        }

        function escapeHtml(value) {
            return String(value).replace(/[&<>"']/g, char => ({
                "&": "&amp;", "<": "&lt;", ">": "&gt;",
                '"': "&quot;", "'": "&#039;"
            })[char]);
        }

        function resetGraph() {
            const nodeUpdates = userNames.map(user => ({
                id: user,
                color: {
                    background: "#168cf0",
                    border: "#8bd5ff",
                    highlight: {background: "#6366f1", border: "#ffffff"},
                    hover: {background: "#38bdf8", border: "#ffffff"}
                }
            }));
            nodes.update(nodeUpdates);

            const edgeUpdates = edges.get().map(edge => ({
                id: edge.id,
                color: "#344765",
                width: 1.4
            }));
            edges.update(edgeUpdates);
            network.fit({animation: true});
        }

        function highlightUsers(selected, source=null, destination=null) {
            resetGraph();

            const selectedSet = new Set(selected);
            const updates = [];

            selectedSet.forEach(user => {
                let background = "#22c55e";
                let border = "#bbf7d0";

                if (user === source) {
                    background = "#06b6d4";
                    border = "#a5f3fc";
                } else if (user === destination) {
                    background = "#f97316";
                    border = "#fed7aa";
                }

                updates.push({
                    id: user,
                    color: {
                        background: background,
                        border: border,
                        highlight: {background: background, border: "#ffffff"}
                    }
                });
            });
            nodes.update(updates);
        }

        function highlightPath(path) {
            if (!path || path.length === 0) return;

            highlightUsers(path, path[0], path[path.length - 1]);

            const pathEdges = [];
            for (let i = 0; i < path.length - 1; i++) {
                pathEdges.push([path[i], path[i + 1]]);
            }

            const updates = edges.get().map(edge => {
                const onPath = pathEdges.some(pair =>
                    (edge.from === pair[0] && edge.to === pair[1]) ||
                    (edge.from === pair[1] && edge.to === pair[0])
                );
                return onPath
                    ? {id: edge.id, color: "#22c55e", width: 5}
                    : {id: edge.id, color: "#344765", width: 1.4};
            });
            edges.update(updates);
        }

        function bfs(start) {
            const visited = new Set([start]);
            const queue = [start];
            const order = [];

            while (queue.length) {
                const current = queue.shift();
                order.push(current);

                [...(graphData[current] || [])].sort().forEach(friend => {
                    if (!visited.has(friend)) {
                        visited.add(friend);
                        queue.push(friend);
                    }
                });
            }
            return order;
        }

        function dfs(start) {
            const visited = new Set();
            const stack = [start];
            const order = [];

            while (stack.length) {
                const current = stack.pop();
                if (visited.has(current)) continue;

                visited.add(current);
                order.push(current);

                [...(graphData[current] || [])].sort().reverse().forEach(friend => {
                    if (!visited.has(friend)) stack.push(friend);
                });
            }
            return order;
        }

        function findShortestPath(start, destination) {
            const queue = [start];
            const parent = {[start]: null};

            while (queue.length) {
                const current = queue.shift();
                if (current === destination) break;

                [...(graphData[current] || [])].sort().forEach(friend => {
                    if (!(friend in parent)) {
                        parent[friend] = current;
                        queue.push(friend);
                    }
                });
            }

            if (!(destination in parent)) return null;

            const path = [];
            let current = destination;
            while (current !== null) {
                path.push(current);
                current = parent[current];
            }
            return path.reverse();
        }

        function mutualFriends(user1, user2) {
            const second = new Set(graphData[user2] || []);
            return (graphData[user1] || []).filter(user => second.has(user)).sort();
        }

        function recommendations(user) {
            const existing = new Set(graphData[user] || []);
            const scores = {};

            (graphData[user] || []).forEach(friend => {
                (graphData[friend] || []).forEach(candidate => {
                    if (candidate === user || existing.has(candidate)) return;

                    const common = mutualFriends(user, candidate).length;
                    scores[candidate] = common;
                });
            });

            return Object.entries(scores).sort((a, b) =>
                b[1] - a[1] || a[0].localeCompare(b[0])
            );
        }

        function connectedComponents() {
            const visited = new Set();
            const components = [];

            userNames.forEach(user => {
                if (visited.has(user)) return;

                const component = [];
                const stack = [user];
                visited.add(user);

                while (stack.length) {
                    const current = stack.pop();
                    component.push(current);

                    (graphData[current] || []).forEach(friend => {
                        if (!visited.has(friend)) {
                            visited.add(friend);
                            stack.push(friend);
                        }
                    });
                }
                components.push(component.sort());
            });
            return components;
        }

        function runAlgorithm() {
            const algorithm = document.getElementById("algorithm").value;
            const start = startSelect.value;
            const end = endSelect.value;

            if (!start) {
                showResult("No users", "The graph contains no users.");
                return;
            }

            if (algorithm === "bfs" || algorithm === "dfs") {
                const order = algorithm === "bfs" ? bfs(start) : dfs(start);
                highlightUsers(order);
                showResult(
                    algorithm === "bfs" ? "BFS traversal order" : "DFS traversal order",
                    order.map((user, index) =>
                        `${index + 1}. ${escapeHtml(user)}`
                    ).join("<br>")
                );
            }

            else if (algorithm === "shortest" || algorithm === "degrees") {
                const path = findShortestPath(start, end);

                if (!path) {
                    resetGraph();
                    showResult("No path found", "These users are not connected.");
                    return;
                }

                highlightPath(path);
                if (algorithm === "shortest") {
                    showResult(
                        "Shortest path",
                        `${path.map(escapeHtml).join(" → ")}<br><br>Path length: ${path.length - 1} connections`
                    );
                } else {
                    showResult(
                        "Degrees of separation",
                        `${escapeHtml(start)} and ${escapeHtml(end)} are ${path.length - 1} connection(s) apart.<br><br>${path.map(escapeHtml).join(" → ")}`
                    );
                }
            }

            else if (algorithm === "mutual") {
                const common = mutualFriends(start, end);
                highlightUsers(common);
                showResult(
                    "Mutual friends",
                    common.length
                        ? `${common.length} mutual friend(s):<br>${common.map(escapeHtml).join("<br>")}`
                        : "No mutual friends found."
                );
            }

            else if (algorithm === "recommend") {
                const list = recommendations(start);
                showResult(
                    `Friend recommendations for ${escapeHtml(start)}`,
                    list.length
                        ? list.map((item, index) =>
                            `${index + 1}. ${escapeHtml(item[0])} — ${item[1]} mutual friend(s)`
                          ).join("<br>")
                        : "No recommendations available."
                );
            }

            else if (algorithm === "connected") {
                const ranked = userNames
                    .map(user => [user, graphData[user].length])
                    .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]));

                highlightUsers(ranked.slice(0, 10).map(item => item[0]));
                showResult(
                    "Most connected users",
                    ranked.slice(0, 20).map((item, index) =>
                        `${index + 1}. ${escapeHtml(item[0])} — ${item[1]} friends`
                    ).join("<br>")
                );
            }

            else if (algorithm === "components") {
                const components = connectedComponents();
                showResult(
                    `Connected components: ${components.length}`,
                    components.map((component, index) =>
                        `<b>Community ${index + 1}</b> (${component.length} users): ${component.slice(0, 15).map(escapeHtml).join(", ")}${component.length > 15 ? " ..." : ""}`
                    ).join("<br><br>")
                );
            }

            else if (algorithm === "statistics") {
                const degrees = userNames.map(user => graphData[user].length);
                const totalEdges = degrees.reduce((sum, degree) => sum + degree, 0) / 2;
                const isolated = userNames.filter(user => graphData[user].length === 0);

                showResult(
                    "Network statistics",
                    `Total users: ${userNames.length}<br>` +
                    `Total friendships: ${totalEdges}<br>` +
                    `Average degree: ${(degrees.reduce((a,b) => a+b, 0) / (userNames.length || 1)).toFixed(2)}<br>` +
                    `Maximum degree: ${Math.max(0, ...degrees)}<br>` +
                    `Minimum degree: ${degrees.length ? Math.min(...degrees) : 0}<br>` +
                    `Users without friends: ${isolated.length}<br>` +
                    `Connected components: ${connectedComponents().length}`
                );
            }
        }

        function sortUsers() {
            const mode = document.getElementById("sortMode").value;
            const sorted = userNames.slice();

            sorted.sort((a, b) => {
                if (mode === "degree_desc") {
                    return graphData[b].length - graphData[a].length || a.localeCompare(b);
                }
                if (mode === "degree_asc") {
                    return graphData[a].length - graphData[b].length || a.localeCompare(b);
                }
                if (mode === "name_desc") return b.localeCompare(a);
                return a.localeCompare(b);
            });

            document.getElementById("sortResult").innerHTML =
                sorted.slice(0, 30).map((user, index) =>
                    `${index + 1}. ${escapeHtml(user)} — ${graphData[user].length} friends`
                ).join("<br>") +
                (sorted.length > 30 ? `<br>...and ${sorted.length - 30} more users` : "");
        }

        sortUsers();
    </script>
    """

    script = (
        script
        .replace("__GRAPH_DATA__", graph_json)
        .replace("__ANALYSIS_DATA__", analysis_json)
    )

    html = html.replace("<body>", "<body>" + dashboard_html)
    html = html.replace("</body>", script + "</body>")

    output_file.write_text(html, encoding="utf-8")
    return str(output_file)
