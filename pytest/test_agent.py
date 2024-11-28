import unittest
import logging
import math
from Objects.Agent import Agent
from Manager.EnvironmentManager import Enviroment
from Objects.Food import Food

# Konfiguriere Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class TestAgent(unittest.TestCase):
    def setUp(self):
        """Set up environment and common objects for tests."""
        self.env = Enviroment()
        logging.info("Environment initialized for tests.")

    def test_agent_move_relative(self):
        agent = Agent(50, 50, 0, 0, 0, noBrain=True, env=self.env)
        agent.moveRelative(1, 1)
        logging.info(f"Agent moved relative to (1, 1), new position: ({agent.x}, {agent.y}).")
        self.assertEqual(agent.x, 51)
        self.assertEqual(agent.y, 51)

    def test_agent_teleport(self):
        agent = Agent(0, 0, 0, 0, 0, noBrain=True, env=self.env)
        agent.teleport(1, 1)
        logging.info(f"Agent teleported to (1, 1), new position: ({agent.x}, {agent.y}).")
        self.assertEqual(agent.x, 1)
        self.assertEqual(agent.y, 1)

    def test_agent_move_relative_by_angle(self):
        agent = Agent(50, 50, 0, 0, 0, noBrain=True, env=self.env)
        self.env.addObjects(agent)
        angle = math.pi / 4
        agent.moveRelativeByAngle(angle, 1)
        logging.info(f"Agent moved by angle {angle}, new position: ({agent.x}, {agent.y}).")
        self.assertAlmostEqual(agent.x, 50 + math.cos(angle), places=5)
        self.assertAlmostEqual(agent.y, 50 + math.sin(angle), places=5)

    def test_agent_feed(self):
        agent = Agent(0, 0, 0, 0, 0, noBrain=True, env=self.env, fooodlevel=0)
        food = Food(0, 0, 0, 0, 0, 10, env=self.env)
        agent.feed(food.foodlevel)
        logging.info(f"Agent fed with {food.foodlevel}, new food level: {agent.foodlevel}.")
        self.assertEqual(agent.foodlevel, 10)

        agent.feed(110)
        logging.info(f"Agent fed with 110, new food level: {agent.foodlevel}.")
        self.assertEqual(agent.foodlevel, 100)

    def test_agent_brain(self):
        agent = Agent(0, 0, 0, 0, 0, noBrain=True, env=self.env)
        self.env.addObjects(agent)
        agent.update()
        logging.info("Agent updated in environment.")
        self.assertEqual(self.env.objects[0].x, 0)
        self.assertEqual(self.env.objects[0].y, 0)

    def test_valid_move(self):
        agent = Agent(0, 0, 0, 0, 0, noBrain=True, env=self.env)
        self.assertTrue(agent.validMove(0, 0))
        self.assertTrue(agent.validMove(50, 50))
        self.assertFalse(agent.validMove(-1, 0))
        self.assertFalse(agent.validMove(0, -1))
        self.assertFalse(agent.validMove(101, 0))
        self.assertFalse(agent.validMove(0, 101))
        logging.info("Valid move tests completed successfully.")

    def test_decrease_food(self):
        agent = Agent(0, 0, 0, 0, 0, noBrain=True, env=self.env, fooodlevel=0)
        agent.decreaseFood()
        logging.info(f"Agent food decreased, new food level: {agent.foodlevel}.")
        self.assertEqual(agent.foodlevel, -1)
        self.assertEqual(len(self.env.eventManager), 1)

    def test_vision_rect(self):
        agent = Agent(50, 50, 0, 10, 10, noBrain=True, env=self.env)
        self.env.addObjects(agent)
        vision = agent.getVission()
        self.assertEqual(vision, [])
        logging.info("Initial vision test passed with empty environment.")

        agent1 = Agent(80, 55, 0, 0, 0, noBrain=True, env=self.env)
        self.env.addObjects(agent1)
        vision_rect = agent.getVisionRect()
        objects_in_vision = len(self.env.quadtree.query(vision_rect))
        logging.info(f"Vision rectangle query returned {objects_in_vision} object(s).")
        self.assertEqual(objects_in_vision, 1)

    def test_filtered_vision(self):
        env = Enviroment()

        # Erstelle den Hauptagenten mit Sichtfeld
        agent = Agent(50, 50, 0, 10, 10, noBrain=True, env=env)
        env.addObjects(agent)

        # Überprüfen, ob die Sicht zu Beginn leer ist
        v = agent.getVission()
        assert v == []

        # Teste für 8 verschiedene Winkel
        angles = [0, 45, 90, 135, 180, 225, 270, 315]
        results = []

        for angle in angles:
            # Setze die Rotation des Hauptagenten
            env.objects[0].r = angle

            # Platziere den zweiten Agenten passend zur Rotation
            if angle == 0:
                agent1 = Agent(80, 55, 0, 0, 0, noBrain=True, env=env)  # Rechts
            elif angle == 45:
                agent1 = Agent(80, 80, 0, 0, 0, noBrain=True, env=env)  # Rechts oben
            elif angle == 90:
                agent1 = Agent(50, 80, 0, 0, 0, noBrain=True, env=env)  # Oben
            elif angle == 135:
                agent1 = Agent(20, 80, 0, 0, 0, noBrain=True, env=env)  # Links oben
            elif angle == 180:
                agent1 = Agent(20, 55, 0, 0, 0, noBrain=True, env=env)  # Links
            elif angle == 225:
                agent1 = Agent(20, 20, 0, 0, 0, noBrain=True, env=env)  # Links unten
            elif angle == 270:
                agent1 = Agent(50, 20, 0, 0, 0, noBrain=True, env=env)  # Unten
            elif angle == 315:
                agent1 = Agent(80, 20, 0, 0, 0, noBrain=True, env=env)  # Rechts unten

            # Füge den zweiten Agenten hinzu und prüfe die Sicht
            env.addObjects(agent1)
            v = env.objects[0].getVission()

            # Überprüfe, ob der Agent korrekt erkannt wurde
            results.append((angle, len(v) == 1))

            # Entferne den zweiten Agenten für den nächsten Test
            env.objects.pop()

    def test_testvision(self):
        agent = Agent(50, 50, 0, 10, 10, fooodlevel=50, noBrain=True, env=self.env)
        self.env.addObjects(agent)

        food = Food(80, 50, 0, 10, 10, 10, env=self.env)
        self.env.addObjects(food)
        vision = agent.getVission()
        logging.info(f"Agent vision detected {len(vision)} object(s).")
        self.assertEqual(len(vision), 1)

        agent.teleport(50, 50, 180)
        logging.info(f"Agent teleported to (50, 50) with rotation {agent.r}.")
        self.assertEqual(agent.r, 180)

        new_food = Food(30, 50, 0, 10, 10, 10, env=self.env)
        self.env.addObjects(new_food)
        vision = agent.getVission()
        logging.info(f"Agent vision after teleport detected {len(vision)} object(s).")
        self.assertEqual(len(vision), 1)

if __name__ == "__main__":
    unittest.main()