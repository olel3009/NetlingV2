from Objects.Object import Object
from Objects.Food import Food
from Manager.CognitiveManager import Brain
from Manager.EventManager import Event, Events
from Manager.QuadTreeManager import rect
import math

class Agent(Object):
    def __init__(self, x, y, r, width, height, fooodlevel = 100, maxfoodlevel = 100, noBrain = False, env = None):
        if env is None and noBrain:
            env = "Playground"
        super().__init__(x, y, r, width, height, env)
        self.logger.debug(f"{self.type} created at ({self.x}, {self.y})")
        self.speed = 1
        self.foodlevel = fooodlevel
        self.maxfoodlevel = maxfoodlevel
        self.noBrain = noBrain
        self.identifier = 0.9
        self.foodDecrease = 0.05
        if not noBrain:
            self.brain = Brain()
        self.distance = {"step": 0, "distance": 0}

    def update(self):
        if self.noBrain:
            return
        # Get the vision of the agent
        x_ratio = 0 if self.x == 0 else self.env.width / self.x
        y_ratio = 0 if self.y == 0 else self.env.height / self.y
        eyes = self.getVission()
        output = self.brain.think([x_ratio, y_ratio, 0 if self.r == 0 else self.r], eyes)

        if output[3] > 0.8:
            #Hit the nearest Player
            self.logger.debug("Hit the nearest Player")
            self.HitTheNearestPlayer(eyes)

        # Move the agent
        self.r = output[0] * 360
        isValid = self.moveRelativeByAngle(self.r, self.speed * output[1])

        #Test if the agent is Alive
        self.distance = {"step": self.distance["step"] + 1, "distance": 0 if not isValid else self.distance["distance"] + (output[1]*self.speed)}

        #Kill the agent if it is not moving
        if self.distance["step"] > 10 and self.distance["distance"] < 2:
            self.foodlevel = 0  #TODO: Change this to a more elegant solution
            self.logger.debug(f"{self.type} died")

        # Calculate the FoodDecrease value
        self.foodDecrease = self.calculateDecreaseValue()

        # Decrease food level
        self.decreaseFood(self.foodDecrease)
        pass

    def HitTheNearestPlayer(self, eyes):
        if len(eyes) == 0: #TODO: Make them not have a Gun :=)
            return False
        nearest = None
        for eye in eyes:
            if eye[2].type == "Agent" and (nearest is None or eye[0] < nearest[0]) and eye[0] < 15:
                nearest = eye
        if nearest is not None:
            nearest[2].foodlevel -= 50 #TODO: Add a Event for this
            self.foodlevel += 50
            print("Hit")
            return True
        return False

    def calculateDecreaseValue(self):
        return 0.05 + (self.distance["distance"] / 100)
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

    def getBiomeUnder(self):
        return self.env.getBiome(self.x, self.y)

    def collect(self):
        return {"x": self.x, "y": self.y, "r": self.r, "width": self.width, "height": self.height, "id": self.id, "type": self.type, "foodlevel": self.foodlevel}

    def collectInDetail(self):
        return {"x": self.x, "y": self.y, "r": self.r, "width": self.width, "height": self.height, "id": self.id, "type": self.type, "foodlevel": self.foodlevel, "brain": self.brain.collect()}