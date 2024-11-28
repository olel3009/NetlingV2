import unittest
from Objects.Object import Object

class TestObject(unittest.TestCase):
    def setUp(self):
        """Setup für jeden Test."""
        self.env = "Playground"  # Eine Beispielumgebung
        self.obj = Object(0, 0, 0, 10, 10, env=self.env)

    def test_initialization(self):
        """Testet die korrekte Initialisierung von Object."""
        self.assertEqual(self.obj.x, 0, "Initial x-coordinate should be 0.")
        self.assertEqual(self.obj.y, 0, "Initial y-coordinate should be 0.")
        self.assertEqual(self.obj.width, 10, "Width should be 10.")
        self.assertEqual(self.obj.height, 10, "Height should be 10.")
        self.assertEqual(self.obj.env, self.env, "Environment should be 'Playground'.")

    def test_set_position(self):
        """Testet das Setzen neuer Positionen."""
        self.obj.x = 100
        self.obj.y = 200
        self.assertEqual(self.obj.x, 100, "x-coordinate was not updated correctly.")
        self.assertEqual(self.obj.y, 200, "y-coordinate was not updated correctly.")

    def test_move_object(self):
        """Testet das Bewegen des Objekts."""
        self.obj.teleport(10, 20)
        self.assertEqual(self.obj.x, 10, "Object x-coordinate after move is incorrect.")
        self.assertEqual(self.obj.y, 20, "Object y-coordinate after move is incorrect.")

    def test_object_to_dict(self):
        """Testet die Umwandlung des Objekts in ein Dictionary."""
        obj_dict = self.obj.collect()
        expected_dict = {
            "x": self.obj.x,
            "y": self.obj.y,
            "r": self.obj.r,
            "width": self.obj.width,
            "height": self.obj.height,
            "id": self.obj.id,
            "type": self.obj.type,
        }
        self.assertEqual(obj_dict, expected_dict, "Object dictionary representation is incorrect.")

    def test_resize(self):
        """Testet das Ändern der Größe des Objekts."""
        self.obj.resize(20, 30)
        self.assertEqual(self.obj.width, 20, "Width after resize is incorrect.")
        self.assertEqual(self.obj.height, 30, "Height after resize is incorrect.")

if __name__ == "__main__":
    unittest.main()
