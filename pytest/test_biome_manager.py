from Manager.BiomeManager import BiomeManager
from Manager.EnvironmentManager import Enviroment
import numpy as np


def test_biome():
    env = Enviroment()
    biomeManager = BiomeManager(env.width, env.height, 2)
    biomeNum = np.unique(biomeManager.biomeMap)
    assert len(biomeNum) == 2, f"Erwartet: 2 Biome, Gefunden: {len(biomeNum)}"

    biomeManager = BiomeManager(env.width, env.height, 3)
    biomeNum = np.unique(biomeManager.biomeMap)
    assert len(biomeNum) == 1, f"Erwartet: 1 Biome, Gefunden: {len(biomeNum)}"

def test_biome_get_at_point():
    env = Enviroment()
    biomeManager = BiomeManager(env.width, env.height, 2)
    assert biomeManager.getBiomeAt(0, 0) == biomeManager.biomeMap[0, 0]
    assert biomeManager.getBiomeAt(50, 50) == biomeManager.biomeMap[50, 50]

def test_biome_sum_ofBiomes():
    env = Enviroment()
    biomeManager = BiomeManager(env.width, env.height, 2)
    assert len(biomeManager.uniqueKeys) == 2

    biomeManager = BiomeManager(env.width, env.height, 3)
    assert len(biomeManager.uniqueKeys) == 1

def test_biome_classes():
    from Biomes.Biome import Biome
    env = Enviroment()
    biomeManager = BiomeManager(env.width, env.height, 2)
    assert len(biomeManager.biomeClasses) == 3
    for classes in biomeManager.biomeClasses:
        assert isinstance(classes, Biome)

def test_biome_class_map():
    env = Enviroment()
    biomeManager = BiomeManager(env.width, env.height, 2)
    assert len(np.unique(biomeManager.biomeMapClass)) == 3