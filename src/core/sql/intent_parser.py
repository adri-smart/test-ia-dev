# KAN-472: Implementar Parser de Intenciones de Consulta
from typing import Dict, Any, List
from src.utils.logging_config import get_logger

logger = get_logger(__name__)

# A mock schema for validation purposes. In a real system, this would be
# dynamically loaded from the database.
DB_SCHEMA = {
    "clientes": {"id", "nombre", "email", "ciudad", "edad"},
    "pedidos": {"id", "cliente_id", "producto_id", "total", "fecha"},
    "productos": {"id", "nombre", "categoria", "precio"},
}

class IntentParser:
    """
    Parses natural language intentions (pre-processed by an LLM)
    into structured parameters for building SQL queries.
    """

    def parse(self, intent_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parses the intent and entities to extract query parameters.

        Args:
            intent_data: A dictionary containing the recognized intent and entities.
                         Example: {
                             "intent": "consulta_pedidos",
                             "entities": [
                                 {"type": "TABLE", "value": "pedidos"},
                                 {"type": "CONDITION", "field": "total", "operator": ">", "value": 500}
                             ]
                         }

        Returns:
            A dictionary with structured query parameters.
        """
        logger.debug(f"Parsing intent data: {intent_data}")

        table = self._extract_table(intent_data.get("entities", []))
        if not table:
            raise ValueError("Could not determine target table from intent.")

        self._validate_table(table)

        conditions = self._extract_conditions(intent_data.get("entities", []))
        self._validate_fields(table, conditions)

        fields = self._extract_fields(intent_data.get("entities", []))
        self._validate_fields(table, fields, is_condition=False)

        parsed_query = {
            "table": table,
            "fields": fields or ["*"],
            "conditions": conditions,
            "aggregations": intent_data.get("aggregations", []),
            "group_by": intent_data.get("group_by", []),
            "order_by": intent_data.get("order_by", []),
        }
        logger.info(f"Parsed query parameters: {parsed_query}")
        return parsed_query

    def _extract_table(self, entities: List[Dict]) -> str:
        for entity in entities:
            if entity.get("type") == "TABLE":
                return entity.get("value")
        return None

    def _extract_conditions(self, entities: List[Dict]) -> List[Dict]:
        return [e for e in entities if e.get("type") == "CONDITION"]

    def _extract_fields(self, entities: List[Dict]) -> List[str]:
        return [e.get("value") for e in entities if e.get("type") == "FIELD"]

    def _validate_table(self, table: str):
        if table not in DB_SCHEMA:
            logger.error(f"Validation Error: Table '{table}' not found in schema.")
            raise ValueError(f"Invalid query: Table '{table}' does not exist.")

    def _validate_fields(self, table: str, items: List[Dict], is_condition=True):
        allowed_fields = DB_SCHEMA[table]
        for item in items:
            field_name = item.get("field") if is_condition else item
            if field_name and field_name not in allowed_fields:
                logger.error(f"Validation Error: Field '{field_name}' not found in table '{table}'.")
                raise ValueError(f"Invalid query: Field '{field_name}' does not exist in table '{table}'.")

# Singleton instance
intent_parser = IntentParser()
