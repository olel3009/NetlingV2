import unittest
import logging
from Manager.IDManager import IDManager

# Logging konfigurieren
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class TestIDManager(unittest.TestCase):
    def setUp(self):
        """Setze die ID-Manager-ID zurück."""
        IDManager.id = 0
        logging.info("IDManager reset to 0.")

    def test_generateID(self):
        """Test, ob IDs korrekt generiert werden."""
        self.assertEqual(IDManager.generateID(), 1, "First generated ID should be 1.")
        self.assertEqual(IDManager.generateID(), 2, "Second generated ID should be 2.")
        logging.info("ID generation Playground passed.")

    def test_resetID(self):
        """Test, ob IDs zurückgesetzt werden können."""
        IDManager.generateID()
        IDManager.generateID()
        logging.info(f"Current ID before reset: {IDManager.id}")
        IDManager.id = 0  # Zurücksetzen
        self.assertEqual(IDManager.generateID(), 1, "After reset, first ID should be 1.")
        logging.info("ID reset Playground passed.")

    def test_generateMultipleIDs(self):
        """Test, ob mehrere IDs in Folge korrekt generiert werden."""
        expected_ids = [1, 2, 3, 4, 5]
        generated_ids = [IDManager.generateID() for _ in range(5)]
        self.assertEqual(generated_ids, expected_ids, "Generated IDs do not match expected sequence.")
        logging.info("Multiple ID generation Playground passed.")

    def test_largeIDGeneration(self):
        """Test, ob IDs auch bei großen Mengen korrekt generiert werden."""
        IDManager.id = 1_000_000  # Starte bei einer großen Zahl
        self.assertEqual(IDManager.generateID(), 1_000_001, "ID generation failed for large starting number.")
        self.assertEqual(IDManager.generateID(), 1_000_002, "Second large ID generation failed.")
        logging.info("Large ID generation Playground passed.")