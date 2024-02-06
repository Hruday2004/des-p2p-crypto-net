from block import Block

class Node:
    def __init__(self, id, coins, isFast, isHighCPU):
        
        self.id = id
        self.coins = coins
        self.isFast = isFast
        self.isHighCPU = isHighCPU
        self.all_transactions   = []
        
        self.already_in_blockchain_transactions = []
        
        self.blocks = {
            0 : [Block(0, 0, 0, -1), 0],
        }
        
        self.longest_blockchain = []
        
    def calculate_longest_blockchain(self):
        
        max_length = 0
        block_id = 0
        
        for id, block in self.blocks.items():
            
            length = block[0].length
            if length > max_length:
                length = max_length
                block_id = id
                
        long_chain = [self.blocks[block_id][0]]
        
        block_id = self.blocks[block_id][0].prev_block
        
        while block_id is not None:
            long_chain.append(self.blocks[block_id][0])
            block_id = self.blocks[block_id][0].prev_block
            
        return long_chain
        
        
                
                

            
        
        