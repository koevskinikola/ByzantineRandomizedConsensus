from byzantinerandomizedconsensus.base.broadcast import IBroadcastHandler
from byzantinerandomizedconsensus.core.brbroadcast import BRBroadcast
from byzantinerandomizedconsensus.utils.messagetype import MessageType


class BRCTest(IBroadcastHandler):
    def deliver(self, message):
        print(message)

host = "127.0.0.1"
N = 4
f = 1
peer_list = list()
nodes = list()

for port in range(7000, (7000 + N)):
    peer_list.append((host, port))

node = BRBroadcast(N, f, 7000, peer_list, BRCTest())
node.broadcast_listener()

# for peer in peer_list:
#     nodes.append(BRBroadcast(N, f, peer[1], peer_list, BRCTest()))
#
# for node in nodes:
#     node.broadcast_listener()
#
# for node in nodes:
#     node.broadcast(MessageType.SEND, "TEST")