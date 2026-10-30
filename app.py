from flask import Flask, render_template, request, redirect, url_for
from collections import deque

app = Flask(__name__)

social_graph = {
    "Alice": ["Bob", "Charlie"],
    "Bob": ["Alice"],
    "Charlie": ["Alice"]
}

@app.route('/')
def home():
    return render_template('index.html', graph=social_graph, path_result=None)

@app.route('/add_user', methods=['POST'])
def add_user():
    username = request.form.get('username')
    if username and username not in social_graph:
        social_graph[username] = []
    return redirect(url_for('home'))

@app.route('/add_friend', methods=['POST'])
def add_friend():
    user1 = request.form.get('user1')
    user2 = request.form.get('user2')
    if user1 and user2 and user1 in social_graph and user2 in social_graph:
        if user1 != user2:
            if user2 not in social_graph[user1]:
                social_graph[user1].append(user2)
            if user1 not in social_graph[user2]:
                social_graph[user2].append(user1)
    return redirect(url_for('home'))

@app.route('/shortest_path', methods=['POST'])
def shortest_path():
    user1 = request.form.get('user1')
    user2 = request.form.get('user2')
    
    path_str = f"No path found between {user1} and {user2}"
    
    if user1 in social_graph and user2 in social_graph:
        # BFS Algorithm for Shortest Path
        queue = deque([[user1]])
        visited = {user1}
        
        found = False
        while queue:
            path = queue.popleft()
            node = path[-1]
            if node == user2:
                path_str = " -> ".join(path) + f" (Degrees: {len(path) - 1})"
                found = True
                break
            for neighbor in social_graph.get(node, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    new_path = list(path)
                    new_path.append(neighbor)
                    queue.append(new_path)
        if not found:
            path_str = f"Users {user1} and {user2} are disconnected."

    return render_template('index.html', graph=social_graph, path_result=path_str)

if __name__ == '__main__':
    app.run(debug=True)