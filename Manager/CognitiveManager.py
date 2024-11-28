import neat
import random
import logging
import os
class Brain:
    def __init__(self, repeatOfMutation=100):
        self.logger = logging.getLogger(__name__)
        # Erstelle ein neues Genom mit einer zufälligen ID
        genome_id = GenomeManagerInstance.generateID()
        # Stelle sicher, dass die Konfiguration korrekt geladen wurde
        if not hasattr(GenomeManagerInstance.NEATConfig, "genome_type"):
            raise ValueError("NEATConfig wurde nicht korrekt initialisiert. Überprüfe den Pfad und die Config-Datei.")

        # Initialisiere das Genom
        self.genome = GenomeManagerInstance.NEATConfig.genome_type(genome_id)
        self.genome.configure_new(GenomeManagerInstance.NEATConfig.genome_config)

        # Erstelle das neuronale Netz
        self.net = neat.nn.FeedForwardNetwork.create(self.genome, GenomeManagerInstance.NEATConfig)
        for _ in range(repeatOfMutation):
            self._apply_mutation(self.genome.mutate_add_connection)


    def think(self, inputs, lens=None):
        """
        Führt eine Entscheidung basierend auf den Eingaben und der Vision des Agents aus.
        """
        inputs1 = []
        if lens:
            for obj in lens:
                inputs1 += self.objToVector(obj)

        # Pad die Inputs auf die erwartete Länge von 12
        inputs1 += [0] * (12 - len(inputs1))
        return self.net.activate(inputs + inputs1)

    def objToVector(self, obj):
        """
        Wandelt ein Objekt in einen Vektor um, der die Distanz, den Winkel und den Typ des Objekts enthält.
        """
        distance = (30 / obj[0]) if obj[0] != 0 else 0
        angle = (360 / obj[1]) if obj[1] != 0 else 0
        object = obj[2]
        type = object.identifier
        return [distance, angle, type]

    def collect(self):
        """
        Sammelt die Informationen des Gehirns in einem Dictionary.
        """
        return self.genome_to_json()

    def mutate_randomly(self, count=1):
        mutation_operations = [
            self.genome.mutate_add_node,
            self.genome.mutate_add_connection,
            self.genome.mutate_delete_node,
            self.genome.mutate_delete_connection
        ]

        success = False
        for _ in range(count):  # Maximal 10 Versuche
            mutation = random.choice(mutation_operations)
            try:
                self._apply_mutation(mutation)
                self.logger.debug(f"Mutation erfolgreich: {mutation}")
                success = True
            except Exception as e:
                self.logger.debug(f"Mutation fehlgeschlagen: {e}")
        if not success:
            self.logger.debug("Mutation fehlgeschlagen. Initialisiere Genom neu.")

        # Netzwerk nach Mutation aktualisieren
        self.net = neat.nn.FeedForwardNetwork.create(self.genome, GenomeManagerInstance.NEATConfig)

    def check_output_connections(self):
        """
        Überprüft, ob jedes Output-Neuron im NEAT-Netzwerk mindestens einmal aktiviert werden kann.
        Testet das Netzwerk mit zufälligen Eingaben und prüft, ob alle Outputs nicht immer Null sind.
        """
        max_tests = 10  # Anzahl der zufälligen Tests

        for test in range(max_tests):
            # Generiere zufällige Eingaben für das Netzwerk
            random_inputs = [random.random() for _ in range(len(self.net.input_nodes))]

            # Aktiviere das Netzwerk
            think = self.net.activate(random_inputs)

            # Protokollierung für Debugging-Zwecke
            self.logger.debug(f"Test {test + 1}/{max_tests}: Outputs: {think}")

            # Wenn alle Outputs 0 sind, ist das Netzwerk nicht vollständig verbunden
            if all(output == 0 for output in think):
                self.logger.warning(f"Test {test + 1}: Outputs sind alle 0. Netzwerk ist nicht vollständig verbunden.")
                return False

        # Alle Tests bestanden
        self.logger.info("Alle Outputs konnten mindestens einmal aktiviert werden.")
        return True

    def _apply_mutation(self, mutation):
        # Prüfe, ob die Mutation `genome_config` erwartet
        if mutation in [self.genome.mutate_add_node, self.genome.mutate_add_connection, self.genome.mutate_delete_node]:
            mutation(GenomeManagerInstance.NEATConfig.genome_config)
        else:
            mutation()
    def genome_to_json(self):
        """Konvertiert ein NEAT-Genom in ein JSON-Format."""
        nodes = []
        connections = []

        # Extrahiere Knoteninformationen
        for node_id, node in self.genome.nodes.items():
            nodes.append({
                "id": node_id,
                "bias": node.bias,
                "activation": node.activation,
                "response": node.response
            })

        # Extrahiere Verbindungen
        for conn_key, conn in self.genome.connections.items():
            if conn.enabled:  # Nur aktive Verbindungen hinzufügen
                connections.append({
                    "input": conn_key[0],
                    "output": conn_key[1],
                    "weight": conn.weight,
                    "enabled": conn.enabled
                })

        # Rückgabe als JSON-kompatibles Dictionary
        return {
            "nodes": nodes,
            "connections": connections
        }

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