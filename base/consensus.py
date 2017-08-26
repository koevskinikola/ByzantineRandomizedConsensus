from abc import ABCMeta, abstractmethod

class Consensus(metaclass=ABCMeta):
    """
    An interface for defining a consensus protocol.
    The 'propose' and 'decide' methods need to be defined
    """

    @abstractmethod
    def propose(self, message):
        #raise NotImplementedError("Method 'propose' needs to be implemented")
        pass

    @abstractmethod
    def decide(self):
        #raise NotImplementedError("Method 'decide' needs to be implemented")
        pass