import logging
from Quadtree import Quadtree, rect
from Event import Event, Events, CollissionEvent
import random
class Enviroment():
    def __init__(self, width = 100, height = 100, agentsCount= 0, foodCount = 0):
        self.objects = []
        self.logger = logging.getLogger(__name__)

        self.width = width
        self.height = height

        self.quadtree = Quadtree(self.width, self.height, 0, 0, 4)
        self.logger.debug("Quadtree created")

        self.eventManager = []
        self.logger.debug("EventManager created")
        self.logger.debug("Enviroment created")

    def addObjects(self, obj):
        self.objects.append(obj)
        self.quadtree.insert(obj)
        self.logger.debug(f"Object added at ({obj.x}, {obj.y})")

    def spawnObjects(self, instance, count = 1, width=10, height=10, rad=None, **kwargs):
        for i in range(count):
            if rad is None:
                x = random.randint(0, self.width)
                y = random.randint(0, self.height)
            else:
                x = random.randint(rad.x, rad.width + rad.x)
                y = random.randint(rad.y, rad.height + rad.y)
            obj = instance(x, y, 0,width, height, env=self, **kwargs)
            self.addObjects(obj)
            self.logger.debug(f"Object spawned at ({obj.x}, {obj.y})")

    def removeObjects(self, obj):
        self.objects.remove(obj)
        self.quadtree.remove(obj)
        self.logger.debug(f"Object removed at ({obj.x}, {obj.y})")

    def update(self):
        for obj in self.objects:
            obj.update()
        self._collissionEvent()
        self.executeEvents()
        self.quadtree.clear()
        for obj in self.objects:
            self.quadtree.insert(obj)
        self.logger.debug("Quadtree updated")

    def collectAll(self):
        return [obj.collect() for obj in self.objects]

    def executeEvents(self):
        for event in self.eventManager:
            if event.event_type == Events.COLLISION:
                event.data[0].onCollission(event.data[1], self.eventManager)
            if event.event_type == Events.DEATH:
                event.data[0].onDeath(event.data[1], self.eventManager)
                self.removeObjects(event.data[0])
        self.eventManager = []

    def _collissionEvent(self):
        for obj in self.objects:
            collision = self._collissionByObjects(obj)
            if collision is not None:
                self.logger.debug(f"Collision detected between {obj.type} and {collision.type}")
                self.eventManager.append(CollissionEvent(obj, collision))

    def _collissionByObjects(self, obj):
        for other in self.objects:
            if other is not obj:
                if (obj.x < other.x + other.width and
                        obj.x + obj.width > other.x and
                        obj.y < other.y + other.height and
                        obj.y + obj.height > other.y):
                    return other
        return None

