import logging
import neat
import os
class IDManager:
    id = 0
    logger = logging.getLogger(__name__)
    @staticmethod
    def generateID():
        IDManager.id += 1
        IDManager.logger.debug(f"ID generated: {IDManager.id}")
        return IDManager.id
