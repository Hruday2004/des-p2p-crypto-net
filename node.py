from cProfile import label
from block import Block
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import os


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
        
        print("Hashing:",self.hashingFraction)
        
        
    def calculate_longest_blockchain(self):

        
        max_length = 0
        block_id = 0
            
        for id, block in self.blocks.items():
            
            length = block[0].length
            # if length != 0 and length == max_length and id != block_id:
            #     print("Same Length Block found")
            if length > max_length:
                max_length = length
                block_id = id
                
        earliest_block_time = self.blocks[block_id][1]
        
        for _, blk in self.blocks.items():
            if blk[0].length == max_length and blk[0].id != block_id and blk[1] < earliest_block_time:
                earliest_block_time = blk[1]
                block_id = blk[0].id
                
                print(f"Same Length Block found for node {self.id}, length: {max_length}")
                
        long_chain = [self.blocks[block_id][0]]
        
        block_id = self.blocks[block_id][0].prev_block_id
        
        while block_id != -1:
            long_chain.append(self.blocks[block_id][0])
            block_id = self.blocks[block_id][0].prev_block_id
            
        return long_chain
    
    def T_k(self):
        return np.random.exponential(3/self.hashingFraction, 1)[0]
    
    def create_chain(self):
        
        file = f"node_{self.id}.dot"
        

        with open(os.path.join("output", file), "w+") as fh:

            # Graphviz header format
            fh.write("digraph G { \n")
            fh.write('rankdir="LR";\n\n')

            # Draw edges of the blockchain tree
            for block in self.blocks.values():

                if block[0].prev_block_id != -1:
                    edge = "\t%d -> %d\n" % (block[0].prev_block_id, block[0].id)

                    fh.write(edge)

                # else:
                #     edge = "%d\n" % block.id

            # Close the graph
            fh.write("\n}")       
            
        for fn in os.listdir("output"):

            if fn.endswith(".dot"):

                fn = os.path.join("output", fn)

                graph = fn[:-4] + ".png"
                cmd = "dot -Tpng %s -o %s" % (fn, graph)

                # TODO: Replace with subprocess.call
                os.system(cmd)
                
        # file1 = f"blocks_arrival_time{self.id}.txt"
        
        # with open(os.path.join("output", file1), "w+") as fh:
        #     for id, bi  in self.blocks.items():
        #         fh.write(f"{id} : {bi[1]} created by {bi[0].node_id}\n")
                
                
        
        
        
        
                
                

            
        
        