# KAN-469, KAN-470: Unit tests for NLP modules
import unittest
from unittest.mock import MagicMock
from src.core.nlp.intent_recognizer import IntentRecognizer
from src.core.nlp.entity_extractor import EntityExtractor

class TestNLP(unittest.TestCase):

    def setUp(self):
        self.mock_llm = MagicMock()
        self.intent_recognizer = IntentRecognizer(self.mock_llm)
        self.entity_extractor = EntityExtractor(self.mock_llm)

    def test_intent_recognition_success(self):
        """KAN-469: Test successful intent recognition."""
        query = "muéstrame las ventas totales del último trimestre"
        self.mock_llm.generate_content.return_value = '{"intent": "consultar_ventas_trimestrales", "confidence": 0.9}'
        
        result = self.intent_recognizer.recognize(query)
        
        self.assertEqual(result['intent'], 'consultar_ventas_trimestrales')
        self.assertGreater(result['confidence'], 0.8)

    def test_intent_recognition_unknown(self):
        """KAN-469: Test handling of ambiguous intent."""
        query = "información general"
        self.mock_llm.generate_content.return_value = '{"intent": "intencion_desconocida", "confidence": 0.4}'

        result = self.intent_recognizer.recognize(query)

        self.assertEqual(result['intent'], 'intencion_desconocida')
        self.assertLess(result['confidence'], 0.5)

    def test_entity_extraction_success(self):
        """KAN-470: Test successful entity extraction."""
        query = "ventas de 'XYZ' el 15 de agosto de 2023"
        self.mock_llm.generate_content.return_value = """
        {
          "entities": [
            {"type": "TABLE", "value": "ventas"},
            {"type": "CONCEPT", "value": "XYZ"},
            {"type": "DATE", "value": "2023-08-15"}
          ]
        }
        """
        
        entities = self.entity_extractor.extract(query)
        
        self.assertEqual(len(entities), 3)
        self.assertIn({"type": "DATE", "value": "2023-08-15"}, entities)

if __name__ == '__main__':
    unittest.main()
