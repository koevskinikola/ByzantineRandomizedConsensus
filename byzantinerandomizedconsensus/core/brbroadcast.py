import json
import socket
import threading

from byzantinerandomizedconsensus.base.broadcast import Broadcast
from byzantinerandomizedconsensus.utils.messagetype import MessageType
from byzantinerandomizedconsensus.utils.enumencoder import EnumEncoder


class BRBroadcast(Broadcast):
    """
    Implements a Byzantine Fault Tolerant Reliable Broadcast protocol.
    """

    def __init__(self, total_nodes, faulty_nodes, host_port, peer_list, consensus_instance):
        """
        Constructs an instance of the Byzantine Reliable Broadcast protocol class.

        :param total_nodes: The total number of nodes in the network. Has to satisfy: N > 3f
        :param faulty_nodes: The maximum number of nodes that may be faulty in the network.
        :param host_port: The port where the instance can be reached.
        :param peer_list: A list of addresses for the rest of the nodes in the network. List of: [(ip, port)}
        :param consensus_instance: The consensus instance for which broadcast is made
        """

        # Make sure that N > 3f
        assert total_nodes > 3*faulty_nodes, "Number of nodes doesn't satisfy N>3f assumption"

        super().__init__(peer_list)

        self.N = total_nodes
        self.f = faulty_nodes
        self.port = host_port
        self.consensus = consensus_instance

        # Check if echo has been sent and collect echo messages
        self.echo_sent_list = dict()

        # Check if ready has been sent and collect ready messages
        self.ready_sent_list = dict()

        # Keep delivered messages
        self.delivered_msgs = list()

    def broadcast_listener(self):
        """
        A TCP socket server for listening to incoming messages

        :return:
        """

        server_listening = True

        host = socket.gethostname()
        broadcast_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        broadcast_server.bind((host, self.port))
        broadcast_server.listen(3 * self.N)

        # do accepts in separate thread
        while server_listening:
            client, address = broadcast_server.accept()
            message = client.recv(BRBroadcast.BUFFER_SIZE)
            if not message:
                print("Message was empty")
            dict_msg = json.loads(message, object_hook=EnumEncoder.as_enum)

            # for local testing
            peer_address = address[0] + ":" + str(address[1])
            # for general use
            # peer_address = address[0]

            # if msg not already delivered
            if dict_msg["message"] not in self.delivered_msgs:

                if dict_msg["type"] == MessageType.SEND and dict_msg["message"] not in self.echo_sent_list:

                    # insert message in dictionary (set ECHO flag to sent)
                    self.echo_sent_list[dict_msg["message"]] = set()

                    # broadcast ECHO msg
                    self.broadcast(MessageType.ECHO, dict_msg["message"])

                elif dict_msg["type"] == MessageType.ECHO:

                    # in case a SEND msg was not received, but ECHO received
                    if dict_msg["message"] not in self.echo_sent_list:
                        self.echo_sent_list[dict_msg["message"]] = set()
                        self.echo_sent_list[dict_msg["message"]].add(peer_address)

                    else:
                        self.echo_sent_list[dict_msg["message"]].add(peer_address)

                        # if more than (N+f)/2 ECHO msgs received, send READY msg
                        if len(self.echo_sent_list[dict_msg["message"]]) > (self.N + self.f) / 2 and dict_msg["message"] not in self.ready_sent_list:
                            self.ready_sent_list[dict_msg["message"]] = set()
                            # broadcast ready msg
                            self.broadcast(MessageType.READY, dict_msg["message"])

                elif dict_msg["type"] == MessageType.READY:

                    # in case a SEND and ECHO msgs were not received, but READY received
                    if dict_msg["message"] not in self.ready_sent_list:
                        self.ready_sent_list[dict_msg["message"]] = set()
                        self.ready_sent_list[dict_msg["message"]].add(peer_address)

                    else:
                        self.ready_sent_list[dict_msg["message"]].add(peer_address)

                        # if 2f READY msgs received, DELIVER msg
                        if len(self.ready_sent_list[dict_msg["message"]]) > 2*self.f:
                            self.delivered_msgs.append(dict_msg["message"])

                            # DELIVER msg to consensus instance
                            self.consensus.deliver(dict_msg["message"])

                        # in case a SEND and ECHO msgs were not received, but f READY msgs received, send READY msg
                        elif dict_msg["message"] not in self.echo_sent_list and len(self.ready_sent_list[dict_msg["message"]]) > self.f:
                            self.broadcast(MessageType.READY, dict_msg["message"])

    # def broadcast_listener(self):
    #     """
    #     Listens for arriving messages from other nodes in the network.
    #     Runs on a separate thread.
    #
    #     :return:
    #     """
    #     threading.Thread(target=self._broadcast_listener).start()
