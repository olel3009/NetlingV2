from Manager.BiomeHelpers.ClusterFinder import ClusterFinder
import numpy as np
import matplotlib.pyplot as plt
from perlin_noise import PerlinNoise

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
        self.biomeMapClass = np.zeros((int(width / self.scaleFactor), int(height / self.scaleFactor)), dtype=int)

        self.cluster = ClusterFinder(self.biomeMap).floodfill()
        self.createBiomeClasses()

    def findScaleFactor(self, width, height):
        """
        Determines an appropriate scale factor for the biome map based on its width.
        """
        if width <= 100:
            return 1
        for factor in range(10, 0, -1):
            if width % factor == 0:
                return factor
        return 1  # Fallback value

    def generateBiomes(self, width, height, numBiomes):
        """
        Generates a biome map using Perlin noise.
        """
        noise = PerlinNoise(octaves=3, seed=42)
        biome_map = np.zeros((width, height), dtype=int)

        for i in range(width):
            for j in range(height):
                value = noise([i / 75, j / 75])  # Scale improves distribution
                biome_map[i, j] = int((value + 1) / 2 * numBiomes) % numBiomes

        return biome_map

    def createBiomeClasses(self):
        """
        Creates biome class instances based on the clustered biomes.
        """
        id_counter = 0
        for i, clusterType in self.cluster.items():
            if i in self.BiomesList:
                biomeClass = self.BiomesList[i]
                for cluster in clusterType.values():
                    self.biomeClasses.append(biomeClass(cluster, id_counter))
                    id_counter += 1

        for biome in self.biomeClasses:
            for clusterCord in biome.cluster:
                self.biomeMapClass[clusterCord[0]][clusterCord[1]] = biome.id

    def visualize_biomes(self):
        """
        Visualizes the biome map using matplotlib.
        """
        plt.imshow(self.biomeMap, cmap='terrain')
        plt.colorbar()
        plt.title('Biome Map')
        plt.show()

    def getBiomeAt(self, x, y):
        """
        Retrieves the biome type at a specific coordinate.
        """
        try:
            return self.biomeMap[int(x / self.scaleFactor), int(y / self.scaleFactor)]
        except IndexError:
            return None

