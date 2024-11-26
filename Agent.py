from Object import Object
from Food import Food
from Brain import Brain
from Event import Event, Events
import math

class Agent(Object):
    def __init__(self, x, y, r, width, height, fooodlevel = 100, maxfoodlevel = 100, noBrain = False, env = None):
        if env is None and noBrain:
            env = "test"
        super().__init__(x, y, r, width, height, env)
        self.logger.debug(f"{self.type} created at ({self.x}, {self.y})")
        self.speed = 1
        self.foodlevel = fooodlevel
        self.maxfoodlevel = maxfoodlevel
        self.noBrain = noBrain
        if not noBrain:
            self.brain = Brain()

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

    def validMove(self, x, y):
        if x < 0 or x > self.env.width or y < 0 or y > self.env.height:
            return False
        return True

    def update(self):
        if self.noBrain:
            return
        r = self.brain.think([self.x, self.y])
        self.moveRelativeByAngle(r[0], self.speed * r[1])
        self.decreaseFood(r[0])
        pass

    def decreaseFood(self, decreaseFaktor=1):
        self.foodlevel -= decreaseFaktor
        if self.foodlevel <= 0:
            self.logger.debug(f"{self.type} died")
            self.env.eventManager.append(Event(Events.DEATH, (self, self)))
        self.logger.debug(f"{self.type} food level is now {self.foodlevel}")

    def onCollission(self, obj, eventManager):
        if isinstance(obj, Food):
            self.logger.debug(f"{self.type} ate {obj.type}")
            self.feed(obj.foodlevel)
            eventManager.append(Event(Events.DEATH, (obj, self)))
        pass

    def feed(self, foodlevel):
        self.foodlevel += foodlevel
        if self.foodlevel > self.maxfoodlevel:
            self.foodlevel = self.maxfoodlevel
        self.logger.debug(f"{self.type} food level is now {self.foodlevel}")

    def collect(self):
        return {"x": self.x, "y": self.y, "r": self.r, "width": self.width, "height": self.height, "id": self.id, "type": self.type, "foodlevel": self.foodlevel}