import neat
import random
import logging
# Lade NEAT-Konfiguration aus der Config-Datei
from Manager.IDManager import GenomeManagerInstance

class Brain:
    def __init__(self, repeatOfMutation=10):
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
        distance = obj[0]
        angle = obj[1]
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