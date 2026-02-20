# KAN-469: Implementar procesamiento básico de consultas en lenguaje natural con LangChain
from typing import Dict, Any
from src.services.gemini import gemini_service
from src.utils.logging_config import get_logger
import json

logger = get_logger(__name__)

class IntentRecognizer:
    """
    Identifies the user's intent from a natural language query using an LLM.
    """

    def __init__(self, llm_service):
        self.llm = llm_service
        self.system_prompt = """
You are an expert at understanding user queries for a business intelligence chatbot.
Your task is to identify the user's main intent from their query.
The possible intents are:
- consultar_ventas_trimestrales
- obtener_producto_mas_vendido
- generar_reporte_regional
- comparar_rendimiento_anual
- proyectar_ingresos_trimestre
- identificar_clientes_valiosos
- segmento_comportamiento_compra
- calcular_tasa_retencion
- analizar_rendimiento_campana
- identificar_clientes_inactivos
- saludo
- despedida
- intencion_desconocida

Based on the user query, respond with a JSON object containing two keys:
1. "intent": The most likely intent from the list above.
2. "confidence": A float between 0.0 and 1.0 indicating your confidence.

If the query is ambiguous, irrelevant, or you cannot determine a clear intent, classify it as "intencion_desconocida" with a confidence score below 0.5.

User Query: "{query}"
JSON Response:
"""

    def recognize(self, query: str) -> Dict[str, Any]:
        """
        Processes a query to identify the main intent.

        Args:
            query: The user's natural language query.

        Returns:
            A dictionary with "intent" and "confidence".
        """
        prompt = self.system_prompt.format(query=query)
        try:
            response_text = self.llm.generate_content(prompt)
            # Clean up the response to make it valid JSON
            cleaned_response = response_text.strip().replace("```json", "").replace("```", "").strip()
            result = json.loads(cleaned_response)
            
            # KAN-469: Validate format
            if "intent" in result and "confidence" in result:
                logger.info(f"Intent recognized for query '{query}': {result}")
                return result
            else:
                logger.warning(f"LLM response for intent recognition is malformed: {result}")
                return {"intent": "intencion_desconocida", "confidence": 0.1}
        except Exception as e:
            logger.error(f"Failed to recognize intent for query '{query}': {e}", exc_info=True)
            return {"intent": "intencion_desconocida", "confidence": 0.0}

# Singleton instance
intent_recognizer = IntentRecognizer(gemini_service)
