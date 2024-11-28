import unittest
import logging
from Manager.EnvironmentManager import Enviroment
from Objects.Agent import Agent

# Konfiguriere Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class TestAgentBrain(unittest.TestCase):
    def setUp(self):
        """Set up a new environment for each test."""
        self.env = Enviroment()
        logging.info("Environment initialized for the test.")

    def test_brain(self):
        """Test the brain's ability to process vision data and generate a vector."""
        # Erstelle Agenten
        agent = Agent(0, 0, 0, 10, 10, noBrain=False, env=self.env)
        agent1 = Agent(20, 0, 0, 10, 10, noBrain=False, env=self.env)

        # Füge beide Agenten zur Umgebung hinzu
        self.env.addObjects(agent)
        self.env.addObjects(agent1)

        # Hole die Sicht des ersten Agenten
        vision = self.env.objects[0].getVission()
        logging.info(f"Agent's vision detected {len(vision)} object(s).")

        # Überprüfe die Sicht
        self.assertEqual(len(vision), 1, "Expected one object in vision.")
        vector = self.env.objects[0].brain.objToVector(vision[0])
        logging.info(f"Object to vector result: {vector}")

        # Überprüfe den berechneten Vektor
        self.assertEqual(vector, [20.0, 0.0, 0.9], "Brain vector computation is incorrect.")

    def test_mutation(self):
        """Test the brain's ability to mutate and generate different outputs."""
        # Erstelle einen Agenten
        agent = Agent(0, 0, 0, 10, 10, noBrain=False, env=self.env)
        self.env.addObjects(agent)

        # Denke mit der aktuellen Gehirnkonfiguration
        initial_thought = agent.brain.think([0, 1], agent.getVission())
        logging.info(f"Initial thought process result: {initial_thought}")

        # Führe Mutationen im Gehirn durch
        agent.brain.mutate_randomly(count=10)
        logging.info("Brain mutated randomly.")

        # Denke erneut mit der mutierten Gehirnkonfiguration
        mutated_thought = agent.brain.think([0, 1], agent.getVission())
        logging.info(f"Mutated thought process result: {mutated_thought}")

        # Stelle sicher, dass die Ergebnisse unterschiedlich sind
        self.assertNotEqual(initial_thought, mutated_thought, "Brain mutation did not change the thought process.")

if __name__ == "__main__":
    unittest.main()