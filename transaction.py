class Transaction:
    def __init__(self, id, sender_id, receiver_id, coins):
        
        self.id = id
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.coins = coins

        self.block_id = None
        
    def __repr__(self):
        return f"TxnID: {self.sender_id} pays {self.receiver_id} {self.coins} coins"