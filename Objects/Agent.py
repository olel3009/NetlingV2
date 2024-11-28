from Objects.Object import Object
from Objects.Food import Food
from Manager.CognitiveManager import Brain
from Manager.EventManager import Event, Events
from Manager.QuadTreeManager import rect
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

    def validMove(self, x, y):
        if x < 0 or x > self.env.width or y < 0 or y > self.env.height:
            return False
        return True

    def update(self):
        if self.noBrain:
            return
        r = self.brain.think([self.x, self.y], self.getVission())
        self.r = r[0] * 360
        self.moveRelativeByAngle(self.r, self.speed * r[1])
        self.decreaseFood(0.2)
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

    def getVisionRect(self):
        vision_distance = 30
        vision_width = vision_distance * math.tan(math.radians(45)) * 2  # 90 degrees FOV
        center_x = self.x + self.width / 2 + vision_distance * math.cos(math.radians(self.r))
        center_y = self.y + self.height / 2 + vision_distance * math.sin(math.radians(self.r))
        rect_x = center_x - vision_width / 2
        rect_y = center_y - vision_distance / 2
        return rect(rect_x, rect_y, vision_width, vision_distance)

    def getVission(self):
        def _isInVissionAngle(obj):
            # Calculate angle to the object
            angle_to_obj = math.degrees(math.atan2(obj.y - self.y, obj.x - self.x)) % 360
            angle_diff = abs((angle_to_obj - self.r + 180) % 360 - 180)
            return angle_diff <= 45  # 90-degree vision cone

        def _isInVissionDistance(obj):
            # Calculate distance to the object
            distance = math.sqrt((obj.x - self.x) ** 2 + (obj.y - self.y) ** 2)
            angle_to_obj = math.degrees(math.atan2(obj.y - self.y, obj.x - self.x)) % 360
            return (distance, angle_to_obj, obj) if distance <= 30 else None

        # Get raw vision objects (tuples from quadtree)
        vision_objects = [entry[1] for entry in self.env.quadtree.query(self.getVisionRect(), 0)]

        # Filter objects in the vision cone and within distance
        filtered_vission = [
            _isInVissionDistance(obj) for obj in vision_objects if _isInVissionAngle(obj)
        ]

        # Remove None values and limit to at most 3 results
        return [v for v in filtered_vission if v is not None][:3]

    def collect(self):
        return {"x": self.x, "y": self.y, "r": self.r, "width": self.width, "height": self.height, "id": self.id, "type": self.type, "foodlevel": self.foodlevel}

    def collectInDetail(self):
        return {"x": self.x, "y": self.y, "r": self.r, "width": self.width, "height": self.height, "id": self.id, "type": self.type, "foodlevel": self.foodlevel, "brain": self.brain.collect()}