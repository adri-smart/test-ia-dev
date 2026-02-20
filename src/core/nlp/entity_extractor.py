# KAN-470: Implementar extracción de entidades clave en consultas de lenguaje natural
from typing import Dict, Any, List
from src.services.gemini import gemini_service
from src.utils.logging_config import get_logger
import json

logger = get_logger(__name__)

class EntityExtractor:
    """
    Extracts key entities from a natural language query using an LLM.
    """

    def __init__(self, llm_service):
        self.llm = llm_service
        self.system_prompt = """
You are an expert entity extractor for a business intelligence chatbot.
Your task is to extract key entities from the user's query.
The possible entity types are:
- TABLE: The database table being queried (e.g., clientes, pedidos).
- FIELD: A specific column in a table (e.g., nombre, total).
- CONDITION: A filter condition, including the field, operator (=, >, <, LIKE), and value.
- PERSON: Name of a person.
- DATE: A specific date, normalized to YYYY-MM-DD format.
- CONCEPT: A business concept or product name.
- NUMBER: A numerical value.

Based on the user query, respond with a JSON object containing a single key "entities", which is a list of extracted entity objects. Each object should have "type", "value", and other relevant fields like "field", "operator" for conditions.

Example Query: "Muéstrame las ventas de Juan Pérez para el producto 'XYZ' el 15 de agosto de 2023 por un total de 5000 dólares"
Example JSON Response:
{
  "entities": [
    {"type": "TABLE", "value": "ventas"},
    {"type": "PERSON", "value": "Juan Pérez"},
    {"type": "CONCEPT", "value": "XYZ"},
    {"type": "DATE", "value": "2023-08-15"},
    {"type": "CONDITION", "field": "total", "operator": "=", "value": 5000}
  ]
}

User Query: "{query}"
JSON Response:
"""

    def extract(self, query: str) -> List[Dict[str, Any]]:
        """
        Processes a query to extract key entities.

        Args:
            query: The user's natural language query.

        Returns:
            A list of dictionaries, each representing an extracted entity.
        """
        prompt = self.system_prompt.format(query=query)
        try:
            response_text = self.llm.generate_content(prompt)
            cleaned_response = response_text.strip().replace("```json", "").replace("```", "").strip()
            result = json.loads(cleaned_response)
            
            # KAN-470: Validate format
            if "entities" in result and isinstance(result["entities"], list):
                logger.info(f"Entities extracted for query '{query}': {result['entities']}")
                return result["entities"]
            else:
                logger.warning(f"LLM response for entity extraction is malformed: {result}")
                return []
        except Exception as e:
            logger.error(f"Failed to extract entities for query '{query}': {e}", exc_info=True)
            return []

# Singleton instance
entity_extractor = EntityExtractor(gemini_service)
