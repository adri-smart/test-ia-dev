# KAN-475: Implementar Validación de Queries SQL y Manejo de Errores
import re
from src.utils.logging_config import get_logger

logger = get_logger(__name__)

class SQLValidator:
    """
    Validates SQL queries against a whitelist of allowed patterns
    to prevent SQL injection and other malicious activities.
    """
    def __init__(self):
        # A simple whitelist. In a real-world scenario, this would be more robust.
        # It allows SELECT statements, basic WHERE clauses, JOINs, GROUP BY, ORDER BY, LIMIT.
        # It explicitly disallows statements that modify data or schema.
        self.allowed_patterns = [
            re.compile(r"^\s*SELECT\s+", re.IGNORECASE),
        ]
        self.disallowed_patterns = [
            re.compile(r"\b(DROP|INSERT|UPDATE|DELETE|TRUNCATE|CREATE|ALTER|EXEC)\b", re.IGNORECASE),
            re.compile(r";"), # Disallow multiple statements
            re.compile(r"--"), # Disallow comments
        ]

    def validate_query(self, query: str) -> bool:
        """
        Validates a SQL query string.

        Args:
            query: The SQL query to validate.

        Returns:
            True if the query is valid, False otherwise.
        """
        # Check for disallowed patterns first
        for pattern in self.disallowed_patterns:
            if pattern.search(query):
                logger.warning(f"SECURITY: Disallowed SQL pattern found in query: {query}")
                return False

        # Check if it matches at least one allowed pattern
        for pattern in self.allowed_patterns:
            if pattern.match(query):
                logger.debug(f"SQL query passed validation: {query}")
                return True

        logger.warning(f"SECURITY: SQL query did not match any allowed patterns: {query}")
        return False

# Singleton instance
sql_validator = SQLValidator()
