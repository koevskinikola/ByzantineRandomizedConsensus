from byzantinerandomizedconsensus.base.consensus import IConsensusHandler
from byzantinerandomizedconsensus.core.byzantinerandomizedconsensus import ByzantineRandomizedConsensus


class Test(IConsensusHandler):

    def __init__(self):

        self.host = "127.0.0.1"
        self.N = 6
        self.f = 1
        self.peer_list = list()
        self.nodes = list()

        for port in range(6000, (6000 + self.N)):
            self.peer_list.append((self.host, port))

        for peer in self.peer_list:
            self.nodes.append(ByzantineRandomizedConsensus(self.N, self.f, self.peer_list, peer[1], self))

        for node in self.nodes:
            node.message_queue.put_nowait(3)

        for node in self.nodes:
            node.start()

    def decide(self, message):
        print("Consensus protocol decided on message: " + message[4] + " from node: " + message[0])