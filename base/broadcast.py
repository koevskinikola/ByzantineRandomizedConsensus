from abc import ABCMeta, abstractmethod
from enum import Enum


class Broadcast(metaclass=ABCMeta):
    """
    An interface for defining a broadcast protocol.
    The 'propose' and 'decide' methods need to be defined
    """

    class MessageType(Enum):
        SEND = 1
        ECHO = 2
        READY = 3

    def __init__(self, node_number, faulty_nodes):
        self.N = node_number
        self.f = faulty_nodes

    @abstractmethod
    def broadcast(self, message):
        pass

    @abstractmethod
    def broadcast_listener(self):
        pass

    @abstractmethod
    def deliver(self, sender, message):
        pass
