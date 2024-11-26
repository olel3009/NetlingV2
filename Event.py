from enum import Enum
class Events(Enum):
    COLLISION = "COLLISION"
    DEATH = "DEATH"

class Event:
    def __init__(self, event_type: Events, data):
        self.event_type = event_type
        self.data = data

class CollissionEvent(Event):
    def __init__(self, obj1, obj2):
        super().__init__(Events.COLLISION, (obj1, obj2))
