import logging

from Manager.IDManager import IDManager
import math
class Object:
    def __init__(self, x, y, r, width, height, env):
        self.logger = logging.getLogger(__name__)
        self.x = x
        self.y = y
        self.r = r
        if env is None and not env=="test":
            self.logger.error("Enviroment is None")
            raise ValueError
        self.env = env
        self.width = width
        self.height = height
        self.id = IDManager.generateID()
        self.type = self.__class__.__name__
        self.identifier = 1
        self.logger.debug(f"{self.type} created at ({self.x}, {self.y})")

    def update(self):
        pass

    def onCollission(self, obj, eventManager):
        pass

    def teleport(self, x, y, r = None):
        self.x = x
        self.y = y
        if r is not None:
            self.r = r
        self.logger.debug(f"{self.type} teleported to ({self.x}, {self.y})")


    def moveRelative(self, dx, dy):
        self.x += dx
        self.y += dy
        if not self.validMove(self.x, self.y):
            self.logger.debug(f"{self.type} can't move to ({self.x}, {self.y})")
            return
        self.logger.debug(f"{self.type} moved to ({self.x}, {self.y})")

    def moveRelativeByAngle(self, angle, distance):
        dx = distance * math.cos(angle)
        dy = distance * math.sin(angle)
        if not self.validMove(self.x + dx, self.y + dy):
            self.logger.debug(f"{self.type} can't move to ({self.x + dx}, {self.y + dy})")
            return
        self.moveRelative(dx, dy)
        self.logger.debug(f"{self.type} moved to ({self.x}, {self.y})")

    def onDeath(self, obj, eventManager):
        pass

    def resize(self, width, height):
        self.width = width
        self.height = height

    def collect(self):
        return {"x": self.x, "y": self.y, "r": self.r, "width": self.width, "height": self.height, "id": self.id, "type": self.type}

    def collectInDetail(self):
        return self.collect()