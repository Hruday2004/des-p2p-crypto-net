from block import Block
import numpy as np

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
        return np.random.exponential(600000/self.hashingFraction, 1)[0]
    
    def create_chain(self):
        pass
        
        
                
                

            
        
        