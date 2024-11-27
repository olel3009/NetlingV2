import logging

from Manager.IDManager import IDManager

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
    def onDeath(self, obj, eventManager):
        pass

    def collect(self):
        return {"x": self.x, "y": self.y, "r": self.r, "width": self.width, "height": self.height, "id": self.id, "type": self.type}

    def collectInDetail(self):
        return self.collect()