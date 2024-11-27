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

class GenomeManager:
    id = 0
    logger = logging.getLogger(__name__)

    def __init__(self):
        config_path = "config-feedforward"  # Stelle sicher, dass der Pfad korrekt ist
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Config-Datei nicht gefunden: {config_path}")

        # Lade die Konfiguration
        self.NEATConfig = neat.Config(
            neat.DefaultGenome,
            neat.DefaultReproduction,
            neat.DefaultSpeciesSet,
            neat.DefaultStagnation,
            config_path,
        )

        # Debugging-Ausgabe
        print(f"Config geladen: num_outputs = {self.NEATConfig.genome_config.num_outputs}")
        print(f"Output Keys: {getattr(self.NEATConfig.genome_config, 'output_keys', 'FEHLT')}")

        # Überprüfe auf fehlende output_keys
        if not hasattr(self.NEATConfig.genome_config, "output_keys"):
            raise ValueError("output_keys wurde nicht generiert. Überprüfe die Config-Datei und Initialisierung.")
    def generateID(self):
        GenomeManager.id += 1
        GenomeManager.logger.debug(f"ID generated: {GenomeManager.id}")
        return GenomeManager.id
GenomeManagerInstance = GenomeManager()