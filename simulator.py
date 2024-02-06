import numpy as np
import random
from node import Node
from queue import PriorityQueue
import networkx as nx
from events import *

class Simulator:
    def __init__(self, num_nodes, slowfrac, lowCPUfrac, txnDelay_meantime):
        self.nodes = self.create_nodes(slowfrac,lowCPUfrac)
        self.peers = self.create_peers(num_nodes)
        self.txnDelay_meantime = txnDelay_meantime
        self.num_nodes = num_nodes
        self.block_id = 1
        self.txn_id = 1

        self.p = []
        self.c = []

        self.time = 0

        self.events = PriorityQueue()

        self.initial_events()

    def __str__(self):
        pass
    def create_nodes(self, slowfrac, lowCPUfrac):

        slownodes = int(slowfrac * self.num_nodes)
        lowCPUnodes = int(lowCPUfrac * self.num_nodes)

        l1 = [1]*slownodes + [0]*int(self.num_nodes-slownodes)
        l2 = [1]*lowCPUnodes + [0]*int(self.num_nodes-lowCPUnodes)

        random.shuffle(l1)
        random.shuffle(l2)

        nodes = {}

        for i in range(self.num_nodes):
            nodes[i] = Node(coins=random.randint(0, 10),isFast=l1[i], isHighCPU=l2[i],id=i)

        for i in range(self.num_nodes):
            self.p.append([])
            self.c.append([])
            for j in range(self.num_nodes):
                self.p[i].append(np.random.uniform(10,500,1)[0])
                if l1[i] == 1 and l1[j] == 1:
                    self.c[i].append(100)
                else:
                    self.c[i].append(5)

        return nodes
    def interArrival_txndelay(self):
        return np.random.exponential(self.txnDelay_meantime, 1)
    
    def create_constrained_graph(self,num_peers):
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

                G.add_edge(peer, connect_to)
              
                possible_connections.remove(connect_to)
        
            if len(connections[peer]) < 3:
                needs_connection.append(peer)
        
        return G
    
    def is_connected(self,G):
        """Checks if the graph is connected."""
        return nx.is_connected(G)

    def create_and_check_constrained_graph(self,num_peers):
        """Recreates the graph until it meets the connected and constraints criteria."""

        while True:
            G = self.create_constrained_graph(num_peers)
            if self.is_connected(G):
                break
        return G
    
    def create_peers(self, num_nodes):
        G = self.create_and_check_constrained_graph(num_nodes)
        peers = {}
        for node in G.nodes():
            peers[node] = list(G.neighbors(node))

        return peers
          
    def initial_events(self):
        for i in range(self.num_nodes):
            self.events.put(TransactionGen(self.interArrival_txndelay, i))
        
        for i in range(self.num_nodes):
            self.events.put(BlockGenReq(,i))

    def run(self):
        # Time updated as events processed
        pass
    def delay(self, message_length,sender_id,receiver_id):
        
        dij = np.random.exponential(96/self.c[sender_id][receiver_id], 1)

        return self.p[sender_id][receiver_id] + message_length/self.c[sender_id][receiver_id] + dij
        

        