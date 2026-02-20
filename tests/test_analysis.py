# KAN-476, KAN-483: Unit tests for analysis modules
import unittest
import pandas as pd
from src.core.analysis.insights_generator import generate_insights
from src.core.analysis.segmentation import filter_by_purchase_behavior

class TestAnalysis(unittest.TestCase):

    def test_generate_insights(self):
        """KAN-476: Test insight generation."""
        data = [85, 92, 78, 95, 88]
        insights = generate_insights(data)
        self.assertGreaterEqual(len(insights), 3)
        
        types = [i['tipo'] for i in insights]
        self.assertIn("Máximo", types)
        self.assertIn("Mínimo", types)
        self.assertIn("Tendencia", types)

    def test_generate_insights_invalid_input(self):
        """KAN-476: Test insight generation with invalid input."""
        with self.assertRaises(ValueError):
            generate_insights([])
        with self.assertRaises(ValueError):
            generate_insights([10, "a", 30])

    def test_purchase_behavior_segmentation(self):
        """KAN-483: Test segmentation for 'bought A not B'."""
        data = {
            'cliente_id': ['c1', 'c2', 'c3', 'c4', 'c5', 'c1', 'c3'],
            'producto_comprado': ['A', 'B', 'A', 'C', 'A', 'C', 'B']
        }
        df = pd.DataFrame(data)
        
        # Expected: c5 bought only A. c1 bought A and C. c3 bought A and B.
        # Result should be ['c5', 'c1']
        result = filter_by_purchase_behavior(df, 'A', 'B')
        
        self.assertCountEqual(result, ['c1', 'c5'])

    def test_purchase_behavior_no_results(self):
        """KAN-483: Test segmentation with no results."""
        data = {
            'cliente_id': ['c2', 'c3'],
            'producto_comprado': ['B', 'B']
        }
        df = pd.DataFrame(data)
        result = filter_by_purchase_behavior(df, 'A', 'B')
        self.assertEqual(result, [])

if __name__ == '__main__':
    unittest.main()
