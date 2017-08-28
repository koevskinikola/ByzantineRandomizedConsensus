from abc import ABCMeta, abstractmethod
import socket, json


class Broadcast(metaclass=ABCMeta):
    """
    An interface for defining a broadcast protocol.
    The 'propose' and 'decide' methods need to be defined
    """

    BUFFER_SIZE = 1024

    def __init__(self, peer_list):
        self.peers = peer_list

    def broadcast(self, message_type, message):
        """
        Sends a message to all of the nodes in the network.

        :param message_type: The type of message to be sent.
        :param message: The message to be sent.
        :return:
        """

        def _broadcast(final_msg):

            final_msg = final_msg.encode('utf-8')

            for addr in self.peers:
                broadcast_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                broadcast_client.connect(addr)
                broadcast_client.sendall(final_msg)
                broadcast_client.shutdown(socket.SHUT_RD)
                broadcast_client.close()

        message = {"peer": socket.gethostname(), "type": message_type, "message": message}
        message = json.dumps(message)

        _broadcast(message)

    @abstractmethod
    def broadcast_listener(self):
        pass


class IBroadcastHandler(metaclass=ABCMeta):
    """
    An interface for providing the deliver event of a broadcast protocol
    """

    @abstractmethod
    def deliver(self, message):
        pass