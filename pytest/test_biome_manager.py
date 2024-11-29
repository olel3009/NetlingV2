from Manager.BiomeManager import BiomeManager
from Manager.EnvironmentManager import Enviroment
import numpy as np


def testBiome():
    env = Enviroment()
    biomeManager = BiomeManager(env.width, env.height, 2)
    biomeNum = np.unique(biomeManager.biomeTypeMap)
    assert len(biomeNum) == 2, f"Erwartet: 2 Biome, Gefunden: {len(biomeNum)}"

    biomeManager = BiomeManager(env.width, env.height, 3)
    biomeNum = np.unique(biomeManager.biomeTypeMap)
    assert len(biomeNum) == 1, f"Erwartet: 1 Biome, Gefunden: {len(biomeNum)}"

def testBiomeGetAtPoint():
    env = Enviroment()
    biomeManager = BiomeManager(env.width, env.height, 2)
    assert biomeManager.getBiomeTypeAt(0, 0) == biomeManager.biomeTypeMap[0, 0]
    assert biomeManager.getBiomeTypeAt(50, 50) == biomeManager.biomeTypeMap[50, 50]

def testBiomeSumOfBiomes():
    env = Enviroment()
    biomeManager = BiomeManager(env.width, env.height, 2)
    assert len(biomeManager.uniqueBiomeTypes) == 2

    biomeManager = BiomeManager(env.width, env.height, 3)
    assert len(biomeManager.uniqueBiomeTypes) == 1

def testBiomeClasses():
    from Biomes.Biome import Biome
    env = Enviroment()
    biomeManager = BiomeManager(env.width, env.height, 2)
    assert len(biomeManager.biomeInstances) == 3
    for classes in biomeManager.biomeInstances:
        assert isinstance(classes, Biome)

def testBiomeClassMap():
    env = Enviroment()
    biomeManager = BiomeManager(env.width, env.height, 2)
    assert len(np.unique(biomeManager.biomeInstanceMap)) == 3
