import networkx as nx
import random
from collections import deque

def create_constrained_graph(num_peers):
    """Creates a graph ensuring each node has 3 to 6 connections."""
    G = nx.Graph()
    G.add_nodes_from(range(num_peers))
    
    # Initialize all nodes with an empty list of connections
    connections = {i: [] for i in range(num_peers)}
    
    # Queue to manage nodes needing more connections
    needs_connection = list(range(num_peers))
    
    while needs_connection:
        peer = needs_connection.pop(0)
        # Ensure we do not exceed the max connections while also meeting the minimum
        possible_connections = [p for p in range(num_peers) if p != peer and len(connections[p]) < 6 and p not in connections[peer]]
        while len(connections[peer]) < 3 and possible_connections:
            # Choose a random peer to connect, ensuring it does not exceed its connection limit
            connect_to = random.choice(possible_connections)
            connections[peer].append(connect_to)
            connections[connect_to].append(peer)
            # Add edge to graph
            G.add_edge(peer, connect_to)
            # If the connected peer now needs more connections, add it back
            # if len(connections[connect_to]) < 3:
            #     needs_connection.append(connect_to)
            # Remove chosen peer from possible connections
            possible_connections.remove(connect_to)
        
        # If still under-connected, add back into the queue for another attempt
        if len(connections[peer]) < 3:
            needs_connection.append(peer)
    
    return G

def is_connected(G):
    """Checks if the graph is connected."""
    return nx.is_connected(G)

def create_and_check_constrained_graph(num_peers):
    """Recreates the graph until it meets the connected and constraints criteria."""
    attempts = 0
    while True:
        attempts += 1
        G = create_constrained_graph(num_peers)
        if is_connected(G):
            break
    return G, attempts


def print_node_peers(G):
    print("Node : Number of Peers")
    l = []
    for node in G.nodes():
        l.append(len(list(G.neighbors(node))))
    print("Max value: ",max(l))
    print("Min_val: ",min(l))

# Call the function with the graph


# Main execution block
if __name__ == "__main__":
    num_peers = 500  # Define the number of peers in the graph
    G_constrained, attempts_constrained = create_and_check_constrained_graph(num_peers)
    print(f"Graph created successfully after {attempts_constrained} attempts.")

    # Optionally, you can include code to visualize the graph using matplotlib
    print_node_peers(G_constrained)
    import matplotlib.pyplot as plt
    plt.figure(figsize=(8, 5))
    nx.draw(G_constrained, with_labels=True, node_color='lightgreen', edge_color='gray')
    plt.title(f"Connected Graph with Constraints (Attempts: {attempts_constrained})")
    plt.show()
