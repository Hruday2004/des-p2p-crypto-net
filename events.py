import random
from transaction import Transaction
from block import Block

class Events:
    def __init__(self, creator_id, exec_node_id, timeOfexec, creation_time):
        self.creator_id = creator_id
        self.exec_node_id = exec_node_id
        self.timeOfexec = timeOfexec
        self.creation_time = creation_time 

    def __lt__(self, other):
        return self.timeOfexec < other.timeOfexec

class TransactionGen(Events):
    def __init__(self, timeOfexec, payer_id, creation_time):
        super().__init__(payer_id,payer_id,timeOfexec, creation_time)
        # Create Txn
        #   |-- payer should be given
        #   |-- txn_amnt randomly generated between [1,payer.curr_balance]w
        # Add Txn_rec event to queue for all peers
        #   |--  calculate delay based on link
        #   |      
        #
        self.payer_id = payer_id
        
    def execute(self, sim):
        payer = sim.nodes[self.payer_id]
        payee_id, payee = random.choice(list(set(list(sim.nodes.items())) - set([(self.payer_id,payer)])))

        if payer.coins == 0:
            return

        amount = random.randint(1,payer.coins)

        payer.coins = payer.coins - amount
        payee.coins = payee.coins + amount

        txn = Transaction(sim.txn_id,self.payer_id,payee_id,amount)

        sim.txn_id+=1

        payer.all_transactions.append(txn)

        for i in sim.peers[self.payer_id]:

            sim.put(TransactionRec(self.timeOfexec + sim.delay(1,self.payer_id,i), i, self.payer_id, self.payer_id, txn,self.creation_time))

        


class TransactionRec(Events):
    def __init__(self, timeOfexec, node_id, creator_id, sender_id, txn, creation_time):
        super().__init__(creator_id, node_id, timeOfexec, creation_time)
        
        self.receiver_id = node_id
        self.transaction = txn
        self.sender_id = sender_id
        
    def execute(self, sim):
        
        rcvr = sim.nodes[self.receiver_id]
        
        if self.transaction in rcvr.all_transactions:
            return
        
        rcvr.all_transactions.append(self.transaction)
        
        for i in sim.peers[self.receiver_id]:
            if i == self.sender_id:
                continue
            sim.put(TransactionRec(self.timeOfexec + sim.delay(1, self.receiver_id, i), i, self.creator_id, self.receiver_id, self.transaction, self.creation_time))
        
        
        
class BlockGen(Events):
    def __init__(self, timeOfexec, creator_id, creation_time, prev_last_block):
        super().__init__(creator_id,creator_id,timeOfexec, creation_time)
        self.prev_last_block = prev_last_block
        
    def execute(self,sim):
        
        
        miner = sim.nodes[self.creator_id]
        new_longest_chain = miner.get_longest_chain()
        
        if(new_longest_chain[0].id != self.prev_last_block.id):
            return
        
        # MINING BEGINS 
        
        remaining_txns = set(miner.all_transactions) - set(miner.already_in_blockchain_transactions)
        
        new_block = Block(sim.block_id, self.exec_node_id, self.timeOfexec, new_longest_chain[0], new_longest_chain[0].length + 1)
        new_block.transactions = list(remaining_txns)
        
        sim.block_id += 1
        
        msg_length = 1 + len(new_block.transactions) 
        
        for i in sim.peers[self.creator_id]:
            sim.put(BlockRec(self.timeOfexec + sim.delay(msg_length, self.creator_id, i), i, self.creator_id, self.timeOfexec, new_block))

class BlockRec(Events):
    def __init__(self, timeOfexec, node_id, creator_id, creation_time, block):
        super().__init__(creator_id, node_id, timeOfexec, creation_time)
        self.block = block
    
    def execute(self,sim):

        if self.block.transactions in sim.nodes[self.exec_node_id].all_transactions:
            return
        
    
        
        longest_chain = sim.nodes[self.exec_node_id].calculate_longest_blockchain()
        last_block = longest_chain[0]

        # validate
        # if valid -- only then send to peers
        # block gen
        

        
        if valid:
            for i in sim.peers[self.exec_node_id]:
                if i == self.exec_node_id:
                    continue
                sim.put(BlockRec(self.timeOfexec + sim.delay(1+len(self.block.transactions), self.exec_node_id, i) , i, self.creator_id, self.timeOfexec, self.block))
        
        sim.events.put(BlockGen(self.timeOfexec + sim.nodes[self.exec_node_id].T_k() , self.exec_node_id , self.timeOfexec, last_block))

        
        

        