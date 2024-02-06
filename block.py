class Block:
    def __init__(self, id, node_id, creation_time, prev_block):
        
        self.id = id
        self.node_id = node_id
        self.creation_time = creation_time
        
        self.transactions = []
        
        self.length = 0
        
        self.prev_block = prev_block
        
    