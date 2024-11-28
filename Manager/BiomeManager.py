from fontTools.ttLib.ttVisitor import visit
from perlin_noise import PerlinNoise
import numpy as np
import matplotlib.pyplot as plt
from Manager.BiomeHelpers.ClusterFinder import ClusterFinder

class Biome:
    def __init__(self, cluster, clusterId):
        self.cluster = cluster
        self.id = clusterId


class Fauna(Biome):
    name = "Fauna"
    def __init__(self, cluster, id):
        super().__init__(cluster, id)

class Savanne(Biome):
    name = "Savanne"
    def __init__(self, cluster, id):
        super().__init__(cluster, id)

class Tundra(Biome):
    name = "Tundra"
    def __init__(self, cluster, id):
        super().__init__(cluster, id)

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
        self.biomeClasses = []
        self.cluster = ClusterFinder(self.biomeMap).floodfill()
        id = 0
        for i, clusterType in enumerate(self.cluster.values()):
            if i in self.BiomesList:
                instance = self.BiomesList[i]
                for cluster in clusterType.values():
                    self.biomeClasses.append(instance(cluster, id))
                    id += 1

        self.biomeMapClass = np.zeros((int(width / self.scaleFactor), int(height / self.scaleFactor)), dtype=int)

        for biome in self.biomeClasses:
            for clusterCord in biome.cluster:
                self.biomeMapClass[clusterCord[0]][clusterCord[1]] = biome.id

    def visualize_biomes(self):
        plt.imshow(self.biomeMap, cmap='terrain')
        plt.colorbar()
        plt.title('Biome Map')
        plt.show()

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

