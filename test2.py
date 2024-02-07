import matplotlib.pyplot as plt
import networkx as nx

# Create a graph
G = nx.DiGraph()

# Add nodes for the blocks with the 'layer' attribute
blocks = 50  # Number of blocks
for i in range(blocks):
    G.add_node(i, label=f"Block {i}")  # Main chain blocks

# Add edges between blocks to represent the chain
for i in range(1, 30):
    G.add_edge(i, i-1)

G.add_edge(30, 29)

for i in range(31, 41):
    G.add_edge(i, i-1)

G.add_edge(41, 29)

for i in range(42, blocks):
    G.add_edge(i, i-1)


# Add edges to represent a fork scenario  # This was already part of your original code

# Orphaned blocks scenario
# Assuming orphaned blocks occur at positions 10, 25, and 35 (for visualization, they are placed near the main chain)
# orphan_blocks = [10, 25, 35]
# for orphan in orphan_blocks:
#     orphan_label = f"Orphan {orphan}"
#     G.add_node(orphan_label, label=orphan_label, layer=orphan - 0.5)  # Slightly offset layer for visualization
#     # No need to connect orphan blocks to the main chain, as they are standalone

# Draw the graph
pos = nx.multipartite_layout(G, subset_key="layer")
plt.figure(figsize=(200, 50))  # Adjust figure size as needed
nx.draw(G, pos, with_labels=True, labels=nx.get_node_attributes(G, 'label'), node_size=3000, node_color="lightblue", font_weight="bold", font_size=10, arrowsize=20)

plt.savefig("blockchain_with_orphans.png", bbox_inches='tight')
