# Social Network Analyzer 

A lightweight, local graph analysis tool and interactive web dashboard built with Python, Flask, and PyVis. This project models social networks using a custom adjacency list, executes graph traversal algorithms, and provides tools for visualizing connections, finding shortest paths, and managing network data.

---

## Features 

- **Custom Graph Data Structure:** Built from scratch using Python dictionaries and sets to efficiently map users and undirected friendships ($O(1)$ average-time lookups).
- **Algorithmic Pathfinding:** Implements **Breadth-First Search (BFS)** to calculate accurate, unweighted shortest paths and degrees of separation between any two users.
- **Influencer Detection:** Automatically analyzes degree distribution across the network to isolate the most connected users.
- **Local Flask Dashboard:** An interactive web interface allowing users to dynamically modify networks, test paths, and view live statistics.
- **Data Persistence:** Built-in JSON import, export, and reset pipelines to save and reload custom network states.
- **Interactive Visualizations:** Generates responsive network graphs using PyVis.

---

## Project Architecture 

```text
       [ test_visualization.html ] 
       (Standalone SNAP Dataset Analyzer)
                    |
      (Operates completely independently)

=======================================================

                     [ graph.py ]
             (Core Data: SocialNetwork Class)
                     /           \
                    /             \
                   v               v
        [ Algorithms.py ]      [ analysis.py ]
        (Shortest Path)        (Network Stats)
                   \               /
                    \             /
                     v           v
                   [ app_3.py ] 
           (Flask Server / Traffic Controller)
                     /           \
                    /             \
                   v               v
    [ visualization.py ]     [ templates/index.html ]
    (PyVis HTML Generator)     (Main User Dashboard)
                   |
                   v
    [ static/social_network.html ]
```

---

## Prerequisites & Installation 

Ensure you have **Python 3.8+** installed on your machine. 

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/social-network-analyzer.git
   cd social-network-analyzer
   ```

2. **Install the required dependencies:**
   ```bash
   pip install flask pyvis networkx
   ```

---

## Running the Application 

1. **Start the Flask development server:**
   ```bash
   python app_3.py
   ```

2. **Open the local dashboard:**
   Open your web browser and navigate to:
   ```text
   http://127.0.0.1:5000
   ```

---

## Team Members 

- **Lokesh** (U25MC001)
- **Aryanandha** (U25MC003)
- **Gehana** (U25MC005)
- **Bhumi** (U25MC030)
- **Hitanshi** (U25MC033)
