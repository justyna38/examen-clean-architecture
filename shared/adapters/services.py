from mdm_core.interfaces.services import IEventPublisher

class InMemoryEventPublisher(IEventPublisher):
    def __init__(self):
        self.events = []
    
    def publish(self, event_type: str, data: dict) -> None:
        self.events.append({"type": event_type, "data": data})