from flask import Flask, flash, redirect, render_template, request, url_for

import visualization

from Algorithms import shortest_path
from analysis import (
    most_connected_users,
    network_statistics,
)
from graph import SocialNetwork

app = Flask(__name__)
app.secret_key = "social-network-analyzer-local-dev-key"

# One in-memory network shared by all routes while the Flask server is running.
social_net = SocialNetwork()


def page_context(path_result=None, highlighted_path=None):
    """Prepare plain data for the Jinja template."""
    graph_data = {
        username: sorted(friends)
        for username, friends in social_net.graph.items()
    }
    stats = network_statistics(social_net)
    max_users = most_connected_users(social_net)

    possible_edges = stats["total_users"] * (stats["total_users"] - 1) / 2
    density = (
        stats["total_friendships"] / possible_edges
        if possible_edges
        else 0
    )
    degree_counts = {}
    for friends in social_net.graph.values():
        degree = len(friends)
        degree_counts[degree] = degree_counts.get(degree, 0) + 1
    max_count = max(degree_counts.values(), default=1)
    degree_distribution = []
    for degree, count in sorted(degree_counts.items()):
        height = (count / max_count) * 100
        degree_distribution.append({
        "degree": degree,
        "count": count,
        "height": height
    })

    return {
        "graph": graph_data,
        "user_count": social_net.get_user_count(),
        "friendship_count": social_net.get_friendship_count(),
        "stats": stats,
        "degree_distribution": degree_distribution,
        "density": density,
        "influencers": max_users,
        "path_result": path_result,
        "highlighted_path": highlighted_path or [],
    }


@app.route("/")
def home():
    return render_template("index.html", **page_context())


@app.route("/run_visualization", methods=["POST"])
def run_visualization():
    """Generate the interactive PyVis network and show it on the dashboard."""
    try:
        visualization.create_visualization(
            social_net,
            output_path=f"{app.static_folder}/social_network.html",
        )
        return render_template(
            "index.html",
            **page_context(),
            visualization_ready=True,
        )
    except Exception as error:
        flash(f"Could not create visualization: {error}", "error")
        return render_template("index.html", **page_context())


@app.route("/add_user", methods=["POST"])
def add_user():
    username = (request.form.get("username") or "").strip()

    if not username:
        flash("Please enter a username.", "error")
    elif social_net.add_user(username):
        flash(f"User '{username}' added successfully.", "success")
    else:
        flash(f"User '{username}' already exists.", "error")

    return redirect(url_for("home"))


@app.route("/add_friend", methods=["POST"])
def add_friend():
    user1 = (request.form.get("user1") or "").strip()
    user2 = (request.form.get("user2") or "").strip()

    if not user1 or not user2:
        flash("Please enter both usernames.", "error")
    elif social_net.add_friendship(user1, user2):
        flash(f"{user1} and {user2} are now friends.", "success")
    elif user1 not in social_net.graph or user2 not in social_net.graph:
        flash("Both users must exist before creating a friendship.", "error")
    elif user1 == user2:
        flash("A user cannot be friends with themselves.", "error")
    else:
        flash("These users are already friends.", "error")

    return redirect(url_for("home"))


@app.route("/shortest_path", methods=["POST"])
def handle_shortest_path():
    user1 = (request.form.get("user1") or "").strip()
    user2 = (request.form.get("user2") or "").strip()

    if not user1 or not user2:
        result = "Please enter both the start and end users."
        path = []
    elif user1 not in social_net.graph:
        result = f"User '{user1}' does not exist."
        path = []
    elif user2 not in social_net.graph:
        result = f"User '{user2}' does not exist."
        path = []
    else:
        path = shortest_path(social_net, user1, user2)
        if path:
            result = " -> ".join(path) + f" (Degrees: {len(path) - 1})"
        else:
            result = f"Users '{user1}' and '{user2}' are disconnected."

    return render_template(
        "index.html",
        **page_context(path_result=result, highlighted_path=path),
    )


if __name__ == "__main__":
    app.run(debug=True)
