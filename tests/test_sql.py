# KAN-473, KAN-475: Unit tests for SQL modules
import unittest
from src.core.sql.query_builder import QueryBuilder
from src.core.sql.security import SQLValidator

class TestSQL(unittest.TestCase):

    def setUp(self):
        self.builder = QueryBuilder()
        self.validator = SQLValidator()

    def test_build_parameterized_query(self):
        """KAN-473: Test building a simple parameterized query."""
        parsed_query = {
            "table": "propiedades",
            "fields": ["*"],
            "conditions": [{"field": "ciudad", "operator": "=", "value": "Madrid"}]
        }
        query, params = self.builder.build(parsed_query)
        self.assertEqual(query, "SELECT * FROM propiedades WHERE ciudad = :param_0")
        self.assertEqual(params, {"param_0": "Madrid"})

    def test_build_in_clause_query(self):
        """KAN-473: Test building a query with an IN clause."""
        parsed_query = {
            "table": "propiedades",
            "fields": ["*"],
            "conditions": [{"field": "ciudad", "operator": "IN", "value": ["Madrid", "Barcelona"]}]
        }
        query, params = self.builder.build(parsed_query)
        self.assertEqual(query, "SELECT * FROM propiedades WHERE ciudad IN (:param_0_0, :param_0_1)")
        self.assertEqual(params, {"param_0_0": "Madrid", "param_0_1": "Barcelona"})

    def test_prevent_sql_injection(self):
        """KAN-473: Test that malicious input is treated as a literal."""
        parsed_query = {
            "table": "propiedades",
            "fields": ["*"],
            "conditions": [{"field": "nombre", "operator": "=", "value": "'' OR 1=1 --"}]
        }
        query, params = self.builder.build(parsed_query)
        self.assertEqual(query, "SELECT * FROM propiedades WHERE nombre = :param_0")
        self.assertEqual(params, {"param_0": "'' OR 1=1 --"})

    def test_sql_validator_allowed(self):
        """KAN-475: Test validator with a safe query."""
        safe_query = "SELECT id, name FROM users WHERE id = 1"
        self.assertTrue(self.validator.validate_query(safe_query))

    def test_sql_validator_disallowed(self):
        """KAN-475: Test validator with a malicious query."""
        unsafe_query = "SELECT id, name FROM users; DROP TABLE users;"
        self.assertFalse(self.validator.validate_query(unsafe_query))
        
        unsafe_query_2 = "UPDATE users SET admin = 1 WHERE id = 1"
        self.assertFalse(self.validator.validate_query(unsafe_query_2))

if __name__ == '__main__':
    unittest.main()
