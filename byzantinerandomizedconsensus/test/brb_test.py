from byzantinerandomizedconsensus.base.broadcast import IBroadcastHandler
from byzantinerandomizedconsensus.core.brbroadcast import BRBroadcast


class BRBTest(IBroadcastHandler):
    def deliver(self, message):
        print(message)

host = "localhost"
N = 4
f = 1
peer_list = list()
nodes = list()

for port in range(5000, (5000 + N)):
    peer_list.append((host, port))

for peer in peer_list:
    nodes.append(BRBroadcast(N, f, peer, peer_list, BRBTest()))

for node in nodes:
    node.broadcast_listener()

i = 0
for node in nodes:
    i = i+1
    node.broadcast(BRBroadcast.SEND, "TEST " + str(i))