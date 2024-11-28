import unittest
import logging
from Manager.EnvironmentManager import Enviroment
from Objects.Object import Object
from Objects.Agent import Agent
from Objects.Food import Food
from Manager.QuadTreeManager import rect

# Logging konfigurieren
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class TestEnvironmentManager(unittest.TestCase):
    def setUp(self):
        """Setup für jeden Test."""
        self.env = Enviroment()
        logging.info("Environment initialized for Playground.")

    def test_addObjects(self):
        """Test, ob Objekte korrekt hinzugefügt werden."""
        obj = Object(10, 10, 0, 0, 0, env=self.env)
        self.env.addObjects(obj)
        logging.info("Object added to environment.")
        self.assertIn(obj, self.env.objects, "Object was not added to environment objects list.")

        range1 = rect(0, 0, self.env.width, self.env.height)
        self.assertEqual(len(self.env.quadtree.query(range1, 0)), 1, "Object not added to quadtree.")

    def test_removeObjects(self):
        """Test, ob Objekte korrekt entfernt werden."""
        obj = Object(0, 0, 0, 0, 0, env=self.env)
        self.env.addObjects(obj)
        self.env.removeObjects(obj)
        logging.info("Object removed from environment.")
        self.assertNotIn(obj, self.env.objects, "Object was not removed from environment objects list.")

    def test_update(self):
        """Test, ob die Umgebung korrekt aktualisiert wird."""
        obj = Object(0, 0, 0, 0, 0, env=self.env)
        self.env.addObjects(obj)
        self.env.objects[0].x = 75
        self.env.objects[0].y = 75
        self.env.update()
        range1 = rect(50, 50, 50, 50)
        self.assertEqual(len(self.env.quadtree.query(range1, 0)), 1, "Object position not updated in quadtree.")

    def test_collission(self):
        """Test, ob Kollisionen korrekt erkannt werden."""
        obj = Object(0, 0, 0, 10, 10, env=self.env)
        obj2 = Object(0, 0, 0, 10, 10, env=self.env)
        self.env.addObjects(obj)
        self.env.addObjects(obj2)

        self.assertEqual(self.env._collissionByObjects(obj), obj2, "Collision not detected correctly.")
        self.assertEqual(self.env._collissionByObjects(obj2), obj, "Collision not detected correctly.")

        obj2.x = 100
        obj2.y = 100
        self.env.update()
        self.assertIsNone(self.env._collissionByObjects(obj), "False collision detected.")
        self.assertIsNone(self.env._collissionByObjects(obj2), "False collision detected.")

    def test_CollissionEvent(self):
        """Test, ob Kollisionsereignisse korrekt erzeugt werden."""
        obj = Object(0, 0, 0, 10, 10, env=self.env)
        obj2 = Object(0, 0, 0, 10, 10, env=self.env)
        self.env.addObjects(obj)
        self.env.addObjects(obj2)
        self.env._collissionEvent()

        self.assertEqual(self.env.eventManager[0].data, (obj, obj2), "Collision event not generated correctly.")

        obj2.x = 100
        obj2.y = 100
        self.env.update()
        self.env._collissionEvent()
        self.assertEqual(len(self.env.eventManager), 0, "Collision event not cleared after objects are apart.")

    def test_Eat(self):
        """Test, ob das Essen von Objekten korrekt funktioniert."""
        agent = Agent(10, 10, 0, 10, 10, noBrain=True, env=self.env, fooodlevel=10)
        food = Food(10, 10, 0, 10, 10, 10, env=self.env)
        self.env.addObjects(agent)
        self.env.addObjects(food)
        self.env.update()

        self.assertEqual(len(self.env.objects), 1, "Food object not consumed.")
        self.assertEqual(agent.foodlevel, 20, "Agent's food level not updated correctly.")

    def test_collectAll(self):
        """Test, ob alle Objekte korrekt gesammelt werden."""
        obj = Object(0, 0, 0, 10, 10, env=self.env)
        self.env.addObjects(obj)
        collected = self.env.collectAll()
        expected = [{"x": 0, "y": 0, "r": 0, "width": 10, "height": 10, "id": obj.id, "type": obj.type}]
        self.assertEqual(collected, expected, "Collected objects do not match.")

        obj1 = Object(0, 0, 0, 10, 10, env=self.env)
        self.env.addObjects(obj1)
        collected = self.env.collectAll()
        expected.append({"x": 0, "y": 0, "r": 0, "width": 10, "height": 10, "id": obj1.id, "type": obj1.type})
        self.assertEqual(collected, expected, "Collected objects do not match after adding a second object.")

    def test_spawn(self):
        """Test, ob Objekte korrekt gespawnt werden."""
        self.env.spawnObjects(Object, 10)
        self.assertEqual(len(self.env.objects), 10, "Spawned objects count does not match.")
