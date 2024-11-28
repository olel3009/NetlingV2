import unittest
from Manager.QuadTreeManager import Quadtree, rect
from Objects.Object import Object

class TestQuadtree(unittest.TestCase):
    def test_quadtree_subdivision(self):
        """Testet die Unterteilung des Quadtrees nach Einfügen von Objekten."""
        qt = Quadtree(100, 100, 0, 0, 3)

        obj2 = Object(25, 25, 0, 0, 0, env="test")
        qt.insert(obj2)

        obj3 = Object(25, 75, 0, 0, 0, env="test")
        qt.insert(obj3)

        obj4 = Object(75, 25, 0, 0, 0, env="test")
        qt.insert(obj4)

        obj5 = Object(75, 75, 0, 0, 0, env="test")
        qt.insert(obj5)

        self.assertTrue(qt.isSubdivided(), "Quadtree should be subdivided after inserting 4 objects.")

    def test_quadtree_insert_and_query(self):
        """Testet das Einfügen und Abfragen von Objekten im Quadtree."""
        qt = Quadtree(100, 100, 0, 0, 4)

        obj = Object(0, 0, 0, 0, 0, env="test")
        qt.insert(obj)

        range1 = rect(0, 0, 100, 100)
        results = qt.query(range1, 0)

        for level, element in results:
            self.assertEqual(element, obj, "Queried object does not match inserted object.")
            self.assertEqual(level, 0, "Queried object level is incorrect.")

    def test_quadtree_query_specific_range(self):
        """Testet das Abfragen eines spezifischen Bereichs im Quadtree."""
        qt = Quadtree(100, 100, 0, 0, 4)

        obj2 = Object(25, 25, 0, 0, 0, env="test")
        qt.insert(obj2)

        obj3 = Object(25, 75, 0, 0, 0, env="test")
        qt.insert(obj3)

        obj4 = Object(75, 25, 0, 0, 0, env="test")
        qt.insert(obj4)

        obj5 = Object(75, 75, 0, 0, 0, env="test")
        qt.insert(obj5)

        obj6 = Object(50, 50, 0, 0, 0, env="test")
        qt.insert(obj6)

        self.assertTrue(qt.isSubdivided(), "Quadtree should be subdivided after inserting multiple objects.")

        range2 = rect(50, 50, 50, 50)
        query_results = qt.query(range2, 0)

        self.assertEqual(len(query_results), 1, "Expected 1 object in the specific range query.")
        self.assertEqual(query_results[0][0], 1, "Queried object level is incorrect.")

