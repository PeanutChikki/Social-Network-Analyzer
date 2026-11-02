from flask import (
    Flask, render_template, request, redirect,
    url_for, flash, send_file
)
from graph import SocialNetwork
from jsonLoader import load_json
from algorithms import shortest_path, degrees_of_separation
from analysis import (
    mutual_friends,
    recommend_friends,
    most_connected_users,
    network_statistics,
    connected_components
)
from visualization import create_visualization

import json
import os
from pathlib import Path
from io import BytesIO


# --------------------------------------------------
# FLASK CONFIGURATION
# --------------------------------------------------

app = Flask(__name__)
app.secret_key = "social-network-analyzer-demo"

BASE_DIR = Path(__file__).resolve().parent
DATASET_PATH = BASE_DIR / "data" / "network.json"
VISUALIZATION_PATH = BASE_DIR / "static" / "social_network.html"

app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024  # 10 MB


# --------------------------------------------------
# LOAD NETWORK
# --------------------------------------------------

social_graph = SocialNetwork()


def load_original_network():
    """Load the original network from network.json."""
    global social_graph

    social_graph = SocialNetwork()
    load_json(social_graph, DATASET_PATH)


load_original_network()


# --------------------------------------------------
# HOME PAGE
# --------------------------------------------------

@app.route("/")
def index():
    """Display the main dashboard."""

    stats = network_statistics(social_graph.graph)
    top_users = most_connected_users(social_graph.graph, 5)

    # Generate the interactive network visualization
    os.makedirs(VISUALIZATION_PATH.parent, exist_ok=True)

    create_visualization(
        social_graph,
        output_path=str(VISUALIZATION_PATH)
    )

    return render_template(
        "index.html",
        graph=social_graph.graph,
        stats=stats,
        top_users=top_users,
        user_count=social_graph.get_user_count(),
        friendship_count=social_graph.get_friendship_count()
    )


# --------------------------------------------------
# ADD USER
# --------------------------------------------------

@app.route("/add_user", methods=["POST"])
def add_user():

    username = request.form.get("username", "").strip()

    try:
        social_graph.add_user(username)
        flash(f"User '{username}' added successfully!", "success")

    except (ValueError, KeyError) as error:
        flash(str(error), "error")

    return redirect(url_for("index"))


# --------------------------------------------------
# REMOVE USER
# --------------------------------------------------

@app.route("/remove_user", methods=["POST"])
def remove_user():

    username = request.form.get("username", "").strip()

    try:
        social_graph.remove_user(username)
        flash(f"User '{username}' removed successfully!", "success")

    except (ValueError, KeyError) as error:
        flash(str(error), "error")

    return redirect(url_for("index"))


# --------------------------------------------------
# ADD FRIENDSHIP
# --------------------------------------------------

@app.route("/add_friend", methods=["POST"])
def add_friend():

    user1 = request.form.get("user1", "").strip()
    user2 = request.form.get("user2", "").strip()

    try:
        social_graph.add_friendship(user1, user2)
        flash("Friendship added successfully!", "success")

    except (ValueError, KeyError) as error:
        flash(str(error), "error")

    return redirect(url_for("index"))


# --------------------------------------------------
# REMOVE FRIENDSHIP
# --------------------------------------------------

@app.route("/remove_friend", methods=["POST"])
def remove_friend():

    user1 = request.form.get("user1", "").strip()
    user2 = request.form.get("user2", "").strip()

    try:
        social_graph.remove_friendship(user1, user2)
        flash("Friendship removed successfully!", "success")

    except (ValueError, KeyError) as error:
        flash(str(error), "error")

    return redirect(url_for("index"))


# --------------------------------------------------
# SHORTEST PATH
# --------------------------------------------------

@app.route("/shortest_path", methods=["POST"])
def find_shortest_path():

    start = request.form.get("start", "").strip()
    end = request.form.get("end", "").strip()

    try:
        path = shortest_path(social_graph.graph, start, end)

        if path:
            flash(
                f"Shortest path: {' → '.join(map(str, path))}",
                "success"
            )
        else:
            flash("No connection found between these users.", "error")

    except (ValueError, KeyError) as error:
        flash(str(error), "error")

    return redirect(url_for("index"))


# --------------------------------------------------
# DEGREES OF SEPARATION
# --------------------------------------------------

@app.route("/degrees", methods=["POST"])
def find_degrees():

    user1 = request.form.get("user1", "").strip()
    user2 = request.form.get("user2", "").strip()

    try:
        degrees = degrees_of_separation(
            social_graph.graph, user1, user2
        )

        flash(f"Degrees of separation: {degrees}", "success")

    except (ValueError, KeyError) as error:
        flash(str(error), "error")

    return redirect(url_for("index"))


# --------------------------------------------------
# MUTUAL FRIENDS
# --------------------------------------------------

@app.route("/mutual_friends", methods=["POST"])
def find_mutual_friends():

    user1 = request.form.get("user1", "").strip()
    user2 = request.form.get("user2", "").strip()

    try:
        result = mutual_friends(social_graph.graph, user1, user2)

        flash(f"Mutual friends: {result}", "success")

    except (ValueError, KeyError) as error:
        flash(str(error), "error")

    return redirect(url_for("index"))


# --------------------------------------------------
# FRIEND RECOMMENDATIONS
# --------------------------------------------------

@app.route("/recommendations", methods=["POST"])
def get_recommendations():

    username = request.form.get("username", "").strip()

    try:
        result = recommend_friends(social_graph.graph, username)

        flash(f"Recommended friends: {result}", "success")

    except (ValueError, KeyError) as error:
        flash(str(error), "error")

    return redirect(url_for("index"))


# --------------------------------------------------
# DOWNLOAD NETWORK
# --------------------------------------------------

@app.route("/download_network")
def download_network():

    # Convert adjacency sets into JSON-compatible lists
    network_data = {
        user: sorted(list(friends))
        for user, friends in social_graph.graph.items()
    }

    json_data = json.dumps(network_data, indent=4)

    file = BytesIO(json_data.encode("utf-8"))
    file.seek(0)

    return send_file(
        file,
        mimetype="application/json",
        as_attachment=True,
        download_name="my_social_network.json"
    )


# --------------------------------------------------
# UPLOAD NETWORK
# --------------------------------------------------

@app.route("/upload_network", methods=["POST"])
def upload_network():

    if "network_file" not in request.files:
        flash("Please select a file.", "error")
        return redirect(url_for("index"))

    file = request.files["network_file"]

    if file.filename == "":
        flash("No file selected.", "error")
        return redirect(url_for("index"))

    if not file.filename.lower().endswith(".json"):
        flash("Please upload a JSON file.", "error")
        return redirect(url_for("index"))

    try:
        data = json.load(file)

        if not isinstance(data, dict):
            raise ValueError("Invalid network format.")

        # Validate the uploaded network
        for user, friends in data.items():

            if not isinstance(user, str) or not isinstance(friends, list):
                raise ValueError("Invalid network structure.")

            if not all(isinstance(friend, str) for friend in friends):
                raise ValueError("Invalid friendship data.")

        # Reconstruct the graph
        new_graph = SocialNetwork()

        for user in data:
            new_graph.add_user(user)

        for user, friends in data.items():
            for friend in friends:

                if user != friend:
                    if friend not in new_graph.graph:
                        new_graph.add_user(friend)

                    new_graph.add_friendship(user, friend)

        global social_graph
        social_graph = new_graph

        flash("Your network was loaded successfully!", "success")

    except (json.JSONDecodeError, ValueError, KeyError) as error:
        flash(f"Could not load network: {error}", "error")

    return redirect(url_for("index"))


# --------------------------------------------------
# RESET NETWORK
# --------------------------------------------------

@app.route("/reset_network", methods=["POST"])
def reset_network():

    load_original_network()

    flash("Network restored to the original dataset.", "success")

    return redirect(url_for("index"))


# --------------------------------------------------
# RUN APPLICATION
# --------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)