from Object import Object
from Food import Food
from Brain import Brain
from Event import Event, Events
from Quadtree import rect
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
        self.identifier = 0.9
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
        r = self.brain.think([self.x, self.y], self.getVission())
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

    import math

    def getVisionRect(self):
        # Sichtweite in Pixel
        vision_distance = 30

        # Breite des Sichtfelds (entsprechend 90 Grad)
        vision_width = vision_distance * math.tan(math.radians(45)) * 2  # 90 Grad Sichtfeld

        # Mittelpunkt des Sichtfelds
        center_x = self.x + self.width / 2 + vision_distance * math.cos(math.radians(self.r))
        center_y = self.y + self.height / 2 + vision_distance * math.sin(math.radians(self.r))

        # Position des Rechtecks (oberer linker Punkt)
        rect_x = center_x - vision_width / 2
        rect_y = center_y - vision_distance / 2  # Zentrierung um die Figur

        # Rechteck erzeugen
        return rect(rect_x, rect_y, vision_width, vision_distance)

    def getVission(self):
        def _isInVissionAngle(obj):
            angle_to_obj = math.atan2(obj.y - self.y, obj.x - self.x)
            angle_diff = abs(angle_to_obj - self.r)
            return angle_diff <= math.pi / 4  # 90 degrees vision cone

        def _isInVissionDistance(obj):
            distance = math.sqrt((obj.x - self.x) ** 2 + (obj.y - self.y) ** 2)
            angle_to_obj = math.atan2(obj.y - self.y, obj.x - self.x)
            return (distance, angle_to_obj, obj) if distance <= 30 else False

        vission = self.env.quadtree.query(self.getVisionRect(), 0)
        filtered_vission = [obj for obj in vission if _isInVissionAngle(obj[1])]
        filtered_vission = [eval for v in filtered_vission if (eval := _isInVissionDistance(v[1]))]

        return filtered_vission[:3] if len(filtered_vission) > 3 else filtered_vission

    def collect(self):
        return {"x": self.x, "y": self.y, "r": self.r, "width": self.width, "height": self.height, "id": self.id, "type": self.type, "foodlevel": self.foodlevel}