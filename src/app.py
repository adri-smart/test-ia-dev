# KAN-471: Integrar módulo de NLP en el flujo de procesamiento de consultas del backend
from flask import Flask, request, jsonify
from src.config import config
from src.utils.logging_config import setup_logging, get_logger
from src.orchestrator.graph import conversational_agent, AgentState
from src.core.sql.database import db_manager
from src.services.gemini import gemini_service

# Setup logging
setup_logging()
logger = get_logger(__name__)

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint to verify service status and connections.
    """
    db_status = db_manager.check_connection()
    gemini_status = gemini_service.health_check()
    
    status = {
        "service": "ok",
        "database_connection": "ok" if db_status else "error",
        "gemini_api_connection": "ok" if gemini_status else "error"
    }
    
    http_status = 200 if db_status and gemini_status else 503
    return jsonify(status), http_status

@app.route('/query', methods=['POST'])
def handle_query():
    """
    Main endpoint to process user queries.
    """
    data = request.get_json()
    if not data or 'query' not in data:
        return jsonify({"error": "Missing 'query' in request body"}), 400

    user_query = data['query']
    logger.info(f"Received query: '{user_query}'")

    # KAN-471: The query is processed by the NLP module (via the orchestrator)
    # The orchestrator handles the full pipeline.
    initial_state = AgentState(query=user_query)
    
    try:
        final_state = conversational_agent.invoke(initial_state)
        logger.info(f"Final agent state: {final_state}")
        
        if final_state.get('error'):
             # Return a user-friendly error, the details are already logged
             return jsonify({"error": "An internal error occurred while processing your request."}), 500

        return jsonify({
            "response": final_state.get('response', "I don't have a response for that."),
            "final_intent": final_state.get('intent'),
        })

    except Exception as e:
        logger.critical(f"Unhandled exception in conversational agent for query '{user_query}': {e}", exc_info=True)
        return jsonify({"error": "A critical error occurred."}), 500

if __name__ == '__main__':
    # For development only. Use Gunicorn in production.
    app.run(host='0.0.0.0', port=5001, debug=True)
