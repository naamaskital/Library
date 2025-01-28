from abc import ABC, abstractmethod

class Observer(ABC):
    @abstractmethod
    def update(self, notification):
        pass
    @abstractmethod
    def get_notifications(self):
        pass
    @abstractmethod
    def clear_notifications(self):
        pass