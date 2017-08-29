import queue
import random
import socket

from byzantinerandomizedconsensus.utils.messagetype import MessageType
from byzantinerandomizedconsensus.base.broadcast import IBroadcastHandler
from byzantinerandomizedconsensus.base.consensus import Consensus
from byzantinerandomizedconsensus.core.brbroadcast import BRBroadcast


class ByzantineRandomizedConsensus(Consensus, IBroadcastHandler):
    """
    Implements a Byzantine Fault Tolerant Randomized Consensus Broadcast protocol.
    """

    def __init__(self, total_nodes, faulty_nodes, peer_list, brb_port, consensus_user):

        assert total_nodes > 5*faulty_nodes, "Number of nodes doesn't satisfy N>5f assumption"

        self.message_queue = queue.Queue(20)
        self.N = total_nodes
        self.f = faulty_nodes
        self.round = 0
        self.phase = 0
        self.message_values = dict()
        self.value_count = 0
        self.received_values = set()
        self.brb = BRBroadcast(total_nodes, faulty_nodes, brb_port, peer_list, self)
        self.consensus_user = consensus_user

        # Start BRBroadcast server
        self.brb.broadcast_listener()

        # for local testing
        self.host_address = socket.gethostname() + ":" + str(self.brb.port)
        # for general use
        # self.host_address = socket.gethostname()

    def start(self):
        proposal = self.message_queue.get_nowait()
        self.propose(proposal)

    def propose(self, message):

        self.round = 1
        self.phase = 1

        #
        self.brb.broadcast(MessageType.SEND,
                           (self.host_address,
                            self.round, MessageType.PHASE1, message))

    def deliver(self, message):
        if message[4] not in self.message_values:
            self.message_values[message[4]] = list()

        self.message_values[message[4]].append(message[0])
        self.value_count += self.value_count + 1
        self.received_values.add(message[4])

        def get_max_val(bound):
            for key, val in self.message_values:
                if len(val) > bound:
                    return key
            return MessageType.NONE

        # End of Phase-1
        if self.value_count > (self.N - self.f) and self.phase == 1:
            proposal = get_max_val((self.N + self.f) / 2)

            self.phase = 2
            self.value_count = 0
            self.message_values.clear()
            self.received_values.clear()

            self.brb.broadcast(MessageType.SEND,
                               (socket.gethostname() + ":" + self.brb.port,
                                self.round, MessageType.PHASE2, proposal))

        # End of Phase-2
        if self.value_count > (self.N - self.f) and self.phase == 2:
            decision = get_max_val(2 * self.f)
            if decision == MessageType.NONE:
                decision = get_max_val(self.f)
                if decision == MessageType.NONE:
                    decision = random.sample(self.received_values, 1)
            else:
                self.consensus_user.decide(decision)

            self.round = self.round + 1
            self.phase = 1
            self.value_count = 0
            self.message_values.clear()
            self.received_values.clear()

            # send decision as next round proposal to help undecided nodes
            self.brb.broadcast(MessageType.SEND,
                               (self.host_address,
                                self.round, MessageType.PHASE1, decision))