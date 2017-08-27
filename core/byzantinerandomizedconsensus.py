from base.consensus import Consensus
import queue


class ByzantineRandomizedConsensus(Consensus):
    """
    Implements a Byzantine Fault Tolerant Randomized Consensus Broadcast protocol.
    """

    def __init__(self):
        self.message_queue = queue.Queue()
        self.round = 0
        self.phase = 0
        self.message_values = dict()
        

    def propose(self, message):
        pass

    def decide(self):
        pass