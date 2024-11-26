from Object import Object
import math

class Agent(Object):
    def __init__(self, x, y, r, width, height):
        super().__init__(x, y, r, width, height)
        self.logger.debug(f"{self.type} created at ({self.x}, {self.y})")
        self.speed = 1

    def teleport(self, x, y, r = None):
        self.x = x
        self.y = y
        if r is not None:
            self.r = r
        self.logger.debug(f"{self.type} teleported to ({self.x}, {self.y})")


    def moveRelative(self, dx, dy):
        self.x += dx
        self.y += dy
        self.logger.debug(f"{self.type} moved to ({self.x}, {self.y})")

    def moveRelativeByAngle(self, angle, distance):
        dx = distance * math.cos(angle)
        dy = distance * math.sin(angle)
        self.moveRelative(dx, dy)
        self.logger.debug(f"{self.type} moved to ({self.x}, {self.y})")