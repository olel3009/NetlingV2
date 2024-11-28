from enum import Enum

class BiomeArt(Enum):
    DESERT = "DESERT"
    Fauna = "FAUNA"
    Tundra = "TUNDRA"

class Biome:
    def __init__(self, biome: BiomeArt):
        self.biome = biome

    def get_biome(self):
        return self.biome

    def set_biome(self, biome):
        self.biome = biome

    def __str__(self):
        return f'{self.biome}'
