import unittest
from unittest import TestLoader

from test_agent import TestAgent
from test_brain import TestAgentBrain
from test_Enviroment import TestEnvironmentManager
from test_IDManager import TestIDManager
from test_object import TestObject
from test_quadtree import TestQuadtree

# Test-Suite manuell erstellen
def Pysuite():
    suite = unittest.TestSuite()
    suite.addTest(TestLoader.loadTestsFromTestCase(TestAgent))
    suite.addTest(TestLoader.loadTestsFromTestCase(TestAgentBrain))
    suite.addTest(TestLoader.loadTestsFromTestCase(TestEnvironmentManager))
    suite.addTest(TestLoader.loadTestsFromTestCase(TestIDManager))
    suite.addTest(TestLoader.loadTestsFromTestCase(TestObject))
    suite.addTest(TestLoader.loadTestsFromTestCase(TestQuadtree))
    return suite

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(Pysuite())
