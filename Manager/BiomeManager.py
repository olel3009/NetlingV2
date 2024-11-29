from Manager.BiomeHelpers.ClusterFinder import ClusterFinder

import numpy as np
import matplotlib.pyplot as plt
from perlin_noise import PerlinNoise
from Biomes.Tundra import Tundra
from Biomes.Fauna import Fauna
from Biomes.Savanne import Savanne


class BiomeManager:
    biomeClassesMapping = {
        0: Fauna,
        1: Savanne,
        2: Tundra
    }

    def __init__(self, mapWidth, mapHeight, numBiomeTypes):
        self.scaleFactor = self.calculateScaleFactor(mapWidth, mapHeight)
        self.biomeTypeMap = self.generateBiomeTypeMap(int(mapWidth / self.scaleFactor),
                                                      int(mapHeight / self.scaleFactor), numBiomeTypes)
        self.uniqueBiomeTypes = np.unique(self.biomeTypeMap)
        self.biomeInstances = []
        self.biomeInstanceMap = np.zeros((int(mapWidth / self.scaleFactor), int(mapHeight / self.scaleFactor)),
                                         dtype=int)

        self.biomeClusters = ClusterFinder(self.biomeTypeMap).floodfill()
        self.createBiomeInstances()

    def calculateScaleFactor(self, mapWidth, mapHeight):
        """
        Determines an appropriate scale factor for the biome map based on its width.
        """
        return 1
        # TODO Fix
        if mapWidth <= 500:
            return 1
        for factor in range(10, 0, -1):
            if mapWidth % factor == 0:
                return factor
        return 1  # Fallback value

    def generateBiomeTypeMap(self, mapWidth, mapHeight, numBiomeTypes):
        """
        Generates a biome type map using Perlin noise.
        """
        noiseGenerator = PerlinNoise(octaves=3, seed=42)
        biomeTypeMap = np.zeros((mapWidth, mapHeight), dtype=int)

        for x in range(mapWidth):
            for y in range(mapHeight):
                noiseValue = noiseGenerator([x / 500, y / 500])  # Scale improves distribution
                biomeTypeMap[x, y] = int((noiseValue + 1) / 2 * numBiomeTypes) % numBiomeTypes

        return biomeTypeMap

    def createBiomeInstances(self):
        """
        Creates biome class instances based on the clustered biomes.
        """
        instanceIdCounter = 0
        for biomeType, clusters in self.biomeClusters.items():
            if biomeType in self.biomeClassesMapping:
                biomeClass = self.biomeClassesMapping[biomeType]
                for clusterCoordinates in clusters.values():
                    self.biomeInstances.append(biomeClass(list(clusterCoordinates), instanceIdCounter))
                    instanceIdCounter += 1

        for biomeInstance in self.biomeInstances:
            for coordinate in biomeInstance.cluster:
                self.biomeInstanceMap[coordinate[0]][coordinate[1]] = biomeInstance.id

    def visualizeBiomeMap(self):
        """
        Visualizes the biome map using matplotlib.
        """
        plt.imshow(self.biomeTypeMap, cmap='terrain')
        plt.colorbar()
        plt.title('Biome Type Map')
        plt.show()

    def getBiomeTypeAt(self, xCoordinate, yCoordinate):
        """
        Retrieves the biome type at a specific coordinate.
        """
        try:
            return self.biomeTypeMap[int(xCoordinate / self.scaleFactor), int(yCoordinate / self.scaleFactor)]
        except IndexError:
            return None
