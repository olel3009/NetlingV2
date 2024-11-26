import logging

from Settings.IDManager import IDManager

class Object:
    def __init__(self, x, y, r, width, height):
        self.logger = logging.getLogger(__name__)
        self.x = x
        self.y = y
        self.r = r
        self.width = width
        self.height = height
        self.id = IDManager.generateID()
        self.type = self.__class__.__name__
        self.logger.debug(f"{self.type} created at ({self.x}, {self.y})")

