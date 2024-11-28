from fontTools.ttLib.ttVisitor import visit
from perlin_noise import PerlinNoise
import numpy as np
import matplotlib.pyplot as plt
from Manager.BiomeHelpers.ClusterFinder import ClusterFinder

class Biome:
    def __init__(self, cluster):
        self.cluster = cluster

class Fauna(Biome):
    name = "Fauna"

class Savanne(Biome):
    name = "Savanne"

class Tundra(Biome):
    name = "Tundra"

class BiomeManager:
    def __init__(self, width, height, numBiomes):
        self.scaleFactor = self.findScaleFactor(width, height)
        self.biomeMap = self.generateBiomes(int(width / self.scaleFactor), int(height / self.scaleFactor), numBiomes)
        self.uniqueKeys = np.unique(self.biomeMap)
        self.BiomesList = {
            0: Fauna,
            1: Savanne,
            2: Tundra
        }
        cluster = ClusterFinder(self.biomeMap).floodfill()
        # Zuteilung der klaster zu den einzelnen biomenCluster zu den Klassen




    def findScaleFactor(self, width, height):
        if width <= 100:
            return 1
        for factor in range(10, 0, -1):
            if width % factor == 0:
                return factor
        return 1  # Fallback-Wert

    def generateBiomes(self, width, height, numBiomes):
        noise = PerlinNoise(octaves=3, seed=42)
        biome_map = np.zeros((width, height), dtype=int)

        for i in range(width):
            for j in range(height):
                value = noise([i / 75, j / 75])  # Skalierung verbessert
                biome_map[i, j] = int((value + 1) / 2 * numBiomes) % numBiomes

        return biome_map

    def getBiomeAt(self, x, y):
        try:
            return self.biomeMap[int(x / self.scaleFactor), int(y / self.scaleFactor)]
        except IndexError:
            return None

