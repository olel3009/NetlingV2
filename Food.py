from Object import Object
class Food(Object):
    def __init__(self, x, y, r, width, height, foodlevel=10, env=None):
        super().__init__(x, y, r, width, height, env)
        self.type = "Food"
        self.foodlevel = foodlevel
        self.logger.debug(f"{self.type} created at ({self.x}, {self.y})")

    def update(self):
        pass

    def onCollission(self, obj, eventManager):
        pass

    def collect(self):
        return {"x": self.x, "y": self.y, "r": self.r, "width": self.width, "height": self.height, "id": self.id, "type": self.type, "foodlevel": self.foodlevel}