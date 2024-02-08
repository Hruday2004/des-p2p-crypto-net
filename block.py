class Block:
    def __init__(self, id, node_id, creation_time, prev_block_id, length):
        
        self.id = id
        self.node_id = node_id
        self.creation_time = creation_time
        
        self.transactions = []
        
        self.length = length
        
        self.prev_block_id = prev_block_id
        
    def __repr__(self):
        return f"block_id: {self.id}, node_id: {self.node_id}, prev_block_id: {self.prev_block_id}, length: {self.length}"