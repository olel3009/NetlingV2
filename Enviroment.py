import logging

class Enviroment():
    def __init__(self):
        self.objects = []
        self.logger = logging.getLogger(__name__)

    def addObjects(self, obj):
        self.objects.append(obj)
        self.logger.debug(f"Object added: {obj.type} at ({obj.x}, {obj.y})")

    