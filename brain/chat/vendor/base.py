from abc import ABC, abstractmethod


class ChatVendor(ABC):
    """
    Base Interface for chat vendors. Implemented by each vendor to provide a consistent interface for handling chat messages.
    """
    @abstractmethod
    def start(self):
        """Start listening. Pass core callback to route messages."""
        pass