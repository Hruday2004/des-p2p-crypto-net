from cProfile import label
from block import Block
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


class Node:
    def __init__(self, id, coins, isFast, isHighCPU, hashingFraction):
        
        self.id = id
        self.coins = coins
        self.isFast = isFast
        self.isHighCPU = isHighCPU
        self.all_transactions   = []
        self.hashingFraction = hashingFraction
        
        self.already_in_blockchain_transactions = []
        
        self.blocks = {
            0 : [Block(0, 0, 0, -1, 0), 0],
        }

        self.layers = {
            0 : [0]
        }
        
        print("Hashing:",self.hashingFraction)
        
        
    def calculate_longest_blockchain(self):

        
        max_length = 0
        block_id = 0
        
        for id, block in self.blocks.items():
            
            length = block[0].length
            if length > max_length:
                length = max_length
                block_id = id
                
        long_chain = [self.blocks[block_id][0]]
        
        block_id = self.blocks[block_id][0].prev_block_id
        
        while block_id != -1:
            long_chain.append(self.blocks[block_id][0])
            block_id = self.blocks[block_id][0].prev_block_id
            
        return long_chain
    
    def T_k(self):
        return np.random.exponential(30000/self.hashingFraction, 1)[0]
    
    def create_chain(self):
        
        G = nx.DiGraph()
        
        G.add_nodes_from([b[0].id for _, b in self.blocks.items()])
        # for l, nodes in self.layers.items():
        #     for n in nodes:
        #         G.add_node(n, lable = f"id: {n}, t: {self.blocks[n][1]}", layer = 1)
                
        for id , b in self.blocks.items():
            if id == 0:
                continue
            G.add_edge(b[0].id, b[0].prev_block_id)
            
        # pos = nx.multipartite_layout(G, subset_key="layer")
        plt.figure(figsize=(200, 50))
        nx.draw(G, with_labels=True, node_size=3000, node_color="lightgreen", font_weight="bold", edge_color= "gray", font_size=20, arrowsize=50)
        # plt.show()
        plt.savefig(f"blockchain_tree_{self.id}", bbox_inches='tight')        
        
        
        
                
                

            
        
        