# KAN-476: Implementar Motor de Transformación de Datos a Insights en Lenguaje Natural
from typing import List, Dict, Any
import numpy as np
from src.utils.logging_config import get_logger

logger = get_logger(__name__)

def generate_insights(data: List[float]) -> List[Dict[str, Any]]:
    """
    Transforms a numerical dataset into structured natural language insights.

    Args:
        data: A list of numerical values.

    Returns:
        A list of dictionaries, where each dictionary is a structured insight.
    """
    if not data or not all(isinstance(x, (int, float)) for x in data):
        # KAN-476: Handle invalid input
        raise ValueError("Input data must be a non-empty list of numbers.")

    insights = []
    np_data = np.array(data)

    # 1. Max insight
    max_val = np.max(np_data)
    insights.append({
        "tipo": "Máximo",
        "valor": float(max_val),
        "descripción": f"El valor más alto alcanzado fue {max_val}, destacándose del resto.",
        "recomendación": "Investigar la causa de este pico para replicar el éxito en el futuro."
    })

    # 2. Min insight
    min_val = np.min(np_data)
    insights.append({
        "tipo": "Mínimo",
        "valor": float(min_val),
        "descripción": f"El punto más bajo registrado fue {min_val}, una posible área de mejora.",
        "recomendación": "Analizar las condiciones de este punto bajo para prevenir futuras caídas."
    })

    # 3. Trend insight (simple linear regression)
    x = np.arange(len(np_data))
    slope, _ = np.polyfit(x, np_data, 1)
    if slope > 0.1:
        trend_desc = "Se observa una tendencia general al alza en los datos."
        trend_reco = "Capitalizar el crecimiento actual y reforzar las estrategias que lo impulsan."
    elif slope < -0.1:
        trend_desc = "Se detecta una tendencia general a la baja en el conjunto de datos."
        trend_reco = "Tomar acciones correctivas para revertir esta tendencia decreciente lo antes posible."
    else:
        trend_desc = "Los datos muestran una tendencia estable sin grandes variaciones generales."
        trend_reco = "Mantener la estrategia actual y monitorear en busca de nuevas oportunidades de crecimiento."
    
    insights.append({
        "tipo": "Tendencia",
        "valor": float(slope),
        "descripción": trend_desc,
        "recomendación": trend_reco
    })

    # 4. Significant Variation insight
    mean_val = np.mean(np_data)
    std_dev = np.std(np_data)
    if mean_val > 0:
        # Check for values that are > 20% different from the mean and also outliers
        for val in np_data:
            if abs(val - mean_val) / mean_val > 0.20 and abs(val - mean_val) > 1.5 * std_dev:
                insights.append({
                    "tipo": "Variación Significativa",
                    "valor": float(val),
                    "descripción": f"El valor {val} representa una variación significativa respecto a la media de {mean_val:.2f}.",
                    "recomendación": "Analizar este valor atípico para entender su causa y posible impacto."
                })
                break # Add only the first significant variation found

    # KAN-476: Validate description format (language, length, no jargon)
    for insight in insights:
        if len(insight["descripción"]) > 100:
            insight["descripción"] = insight["descripción"][:97] + "..."
        if len(insight["recomendación"]) > 15 * 6: # Approx 15 words
             insight["recomendación"] = " ".join(insight["recomendación"].split(" ")[:15]) + "..."

    return insights
