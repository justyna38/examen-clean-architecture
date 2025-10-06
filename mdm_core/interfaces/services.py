from abc import ABC, abstractmethod

class IEventPublisher(ABC):
    @abstractmethod
    def publish(self, event_type: str, data: dict) -> None:
        pass