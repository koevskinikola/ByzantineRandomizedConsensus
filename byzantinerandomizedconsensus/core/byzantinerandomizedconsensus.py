import queue
import random
import json

from byzantinerandomizedconsensus.base.broadcast import IBroadcastHandler
from byzantinerandomizedconsensus.base.consensus import Consensus
from byzantinerandomizedconsensus.core.brbroadcast import BRBroadcast


class ByzantineRandomizedConsensus(Consensus, IBroadcastHandler):
    """
    Implements a Byzantine Fault Tolerant Randomized Consensus Broadcast protocol.
    """
    NONE = -1
    PHASE1 = 1
    PHASE2 = 2

    def __init__(self, total_nodes, faulty_nodes, peer_list, host_address, consensus_user):

        assert total_nodes > 5*faulty_nodes, "Number of nodes doesn't satisfy N>5f assumption"

        self.message_queue = queue.Queue(20)
        self.N = total_nodes
        self.f = faulty_nodes
        self.round = 0
        self.phase = 0
        self.message_values = dict()
        self.value_count = 0
        self.received_values = set()
        self.brb = BRBroadcast(total_nodes, faulty_nodes, host_address, peer_list, self)
        self.consensus_user = consensus_user

        # Start BRBroadcast server
        self.brb.broadcast_listener()

        self.host_address = host_address

    def start(self):
        proposal = self.message_queue.get_nowait()
        print("Consensus started on " + str(self.host_address))
        self.propose(proposal)

    def propose(self, message):
        message = str(message)
        self.round = 1
        self.phase = 1

        message = {"host": self.host_address, "round": self.round, "phase": ByzantineRandomizedConsensus.PHASE1, "message": message}
        message = json.dumps(message)
        self.brb.broadcast(BRBroadcast.SEND, message)
        print("Proposal sent on " + str(self.host_address))

    def deliver(self, message):
        dict_message = json.loads(message)
        dict_message["host"] = frozenset(dict_message["host"])

        if dict_message["message"] not in self.message_values:
            self.message_values[dict_message["message"]] = set()

        self.message_values[dict_message["message"]].add(dict_message["host"])
        self.value_count = self.value_count + 1
        self.received_values.add(dict_message["message"])

        def get_max_val(bound):
            for key in self.message_values:
                if len(self.message_values[key]) > bound:
                    return key
            return str(ByzantineRandomizedConsensus.NONE)

        # End of Phase-1
        if self.value_count > (self.N - self.f) and self.phase == 1:
            # print(self.message_values)
            proposal = get_max_val((self.N + self.f) / 2)

            self.phase = 2
            self.value_count = 0
            self.message_values.clear()
            self.received_values.clear()

            proposal = {"host": self.host_address, "round": self.round, "phase": ByzantineRandomizedConsensus.PHASE2, "message": proposal}
            proposal = json.dumps(proposal)

            self.brb.broadcast(BRBroadcast.SEND, proposal)

        # End of Phase-2
        if self.value_count > (self.N - self.f) and self.phase == 2:
            # print(self.message_values)
            decision = get_max_val(2 * self.f)
            if decision == ByzantineRandomizedConsensus.NONE:
                decision = get_max_val(self.f)
                if decision == ByzantineRandomizedConsensus.NONE:
                    decision = random.sample(self.received_values, 1)
            else:
                self.consensus_user.decide(decision)

            self.round = self.round + 1
            self.phase = 1
            self.value_count = 0
            self.message_values.clear()
            self.received_values.clear()

            decision = {"host": self.host_address, "round": self.round, "phase": ByzantineRandomizedConsensus.PHASE1, "message": decision}
            decision = json.dumps(decision)

            # send decision as next round proposal to help undecided nodes
            self.brb.broadcast(BRBroadcast.SEND, decision)
