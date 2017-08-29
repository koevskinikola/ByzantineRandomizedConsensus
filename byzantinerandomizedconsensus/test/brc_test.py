from byzantinerandomizedconsensus.base.consensus import IConsensusHandler
from byzantinerandomizedconsensus.core.byzantinerandomizedconsensus import ByzantineRandomizedConsensus
import random


class BRCTest(IConsensusHandler):

    def decide(self, message):
        print("Consensus protocol decided on message: " + message)


host = "localhost"
N = 6
f = 1
start_port = 5555
peer_list = list()
nodes = list()

for port in range(start_port, (start_port + N)):
    peer_list.append((host, port))

for peer in peer_list:
    nodes.append(ByzantineRandomizedConsensus(N, f, peer_list, peer, BRCTest()))

for node in nodes:
    node.message_queue.put_nowait(3)
    node.start()