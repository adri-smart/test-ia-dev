# KAN-477, KAN-478, KAN-479: LangGraph Conversational Orchestrator
from typing import List, Dict, Any
from langgraph.graph import StateGraph, END
from src.core.nlp.intent_recognizer import intent_recognizer
from src.core.nlp.entity_extractor import entity_extractor
from src.core.sql.intent_parser import intent_parser
from src.core.sql.query_builder import query_builder
from src.core.sql.security import sql_validator
from src.core.sql.database import db_manager
from src.core.analysis.insights_generator import generate_insights
from src.utils.logging_config import get_logger

logger = get_logger(__name__)

# KAN-477: Define the state of the conversation
class AgentState(Dict):
    query: str
    intent: str
    entities: List[Dict]
    sql_query: str
    sql_params: Dict
    db_results: List[Dict]
    insights: List[Dict]
    response: str
    error: str = None

# Define node functions
def recognize_intent_node(state: AgentState):
    logger.info("Node: recognize_intent")
    query = state['query']
    intent_result = intent_recognizer.recognize(query)
    state['intent'] = intent_result['intent']
    return state

def extract_entities_node(state: AgentState):
    logger.info("Node: extract_entities")
    query = state['query']
    state['entities'] = entity_extractor.extract(query)
    return state

def build_sql_node(state: AgentState):
    logger.info("Node: build_sql")
    try:
        # KAN-479: Invoke external services (parsers, builders)
        parsed_intent = {"intent": state['intent'], "entities": state['entities']}
        parsed_query = intent_parser.parse(parsed_intent)
        sql, params = query_builder.build(parsed_query)
        
        # KAN-475: Validate SQL before execution
        if not sql_validator.validate_query(sql):
            raise PermissionError("Generated SQL query is not allowed.")
            
        state['sql_query'] = sql
        state['sql_params'] = params
        state['error'] = None
    except Exception as e:
        logger.error(f"Error in build_sql_node: {e}")
        state['error'] = str(e)
    return state

def execute_sql_node(state: AgentState):
    logger.info("Node: execute_sql")
    try:
        results = db_manager.execute_query(state['sql_query'], state['sql_params'])
        state['db_results'] = results
        state['error'] = None
    except Exception as e:
        logger.error(f"Error in execute_sql_node: {e}")
        state['error'] = str(e)
    return state

def generate_insights_node(state: AgentState):
    logger.info("Node: generate_insights")
    try:
        # Assuming results are numerical for insight generation
        # This is a simplification; a real implementation would be more complex
        numerical_data = [float(row['total']) for row in state['db_results'] if 'total' in row]
        if numerical_data:
            state['insights'] = generate_insights(numerical_data)
        else:
            state['insights'] = []
        state['error'] = None
    except Exception as e:
        logger.error(f"Error in generate_insights_node: {e}")
        state['error'] = str(e)
    return state

def format_response_node(state: AgentState):
    logger.info("Node: format_response")
    if state.get('error'):
        state['response'] = f"Lo siento, ocurrió un error: {state['error']}"
    elif state.get('insights'):
        response_parts = ["Aquí tienes los insights encontrados:"]
        for insight in state['insights']:
            response_parts.append(f"- {insight['descripción']} {insight['recomendación']}")
        state['response'] = "\n".join(response_parts)
    elif state.get('db_results'):
        response_parts = [f"Encontré {len(state['db_results'])} resultados:"]
        # Limiting output for brevity
        for row in state['db_results'][:5]:
            response_parts.append(str(dict(row)))
        if len(state['db_results']) > 5:
            response_parts.append("...")
        state['response'] = "\n".join(response_parts)
    else:
        state['response'] = "No pude encontrar resultados para tu consulta."
    return state

# KAN-478: Define conditional edges for transitions
def route_after_intent(state: AgentState):
    intent = state.get('intent', 'intencion_desconocida')
    if intent in ['saludo', 'despedida', 'intencion_desconocida']:
        return "end_conversation"
    if intent in ['consultar_ventas_trimestrales', 'obtener_producto_mas_vendido', 'identificar_clientes_valiosos']:
        return "extract_entities"
    return "end_conversation" # Default fallback

def route_after_sql_build(state: AgentState):
    if state.get('error'):
        return "format_response" # Go to format error response
    return "execute_sql"

def route_after_sql_execution(state: AgentState):
    if state.get('error'):
        return "format_response"
    if state.get('db_results'):
        # Decide if insights are needed
        if state['intent'] in ['comparar_rendimiento_anual']:
             return "generate_insights"
        return "format_response"
    return "format_response" # No results

# Build the graph
workflow = StateGraph(AgentState)

workflow.add_node("recognize_intent", recognize_intent_node)
workflow.add_node("extract_entities", extract_entities_node)
workflow.add_node("build_sql", build_sql_node)
workflow.add_node("execute_sql", execute_sql_node)
workflow.add_node("generate_insights", generate_insights_node)
workflow.add_node("format_response", format_response_node)

workflow.set_entry_point("recognize_intent")

workflow.add_conditional_edges(
    "recognize_intent",
    route_after_intent,
    {
        "extract_entities": "extract_entities",
        "end_conversation": END # Simplified: end if intent is simple
    }
)
workflow.add_edge("extract_entities", "build_sql")
workflow.add_conditional_edges("build_sql", route_after_sql_build, {
    "execute_sql": "execute_sql",
    "format_response": "format_response"
})
workflow.add_conditional_edges("execute_sql", route_after_sql_execution, {
    "generate_insights": "generate_insights",
    "format_response": "format_response"
})
workflow.add_edge("generate_insights", "format_response")
workflow.add_edge("format_response", END)

# Compile the graph
conversational_agent = workflow.compile()
logger.info("Conversational agent graph compiled successfully.")
