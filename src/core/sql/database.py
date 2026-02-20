# KAN-467: Configurar Conexión a Base de Datos de Clientes
# KAN-474: Ejecutar y Validar Resultados de Consultas SQL
# KAN-465: Implementar Sistema de Logging y Monitoreo de Consultas
import time
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from src.config import config
from src.utils.logging_config import get_logger

logger = get_logger(__name__)

class DatabaseManager:
    """
    Manages the database connection, query execution, and logging.
    """
    def __init__(self, db_url: str):
        try:
            self.engine = create_engine(db_url, pool_pre_ping=True)
            logger.info("Database engine created.")
        except Exception as e:
            logger.critical(f"Failed to create database engine: {e}")
            raise

    def check_connection(self) -> bool:
        """
        Verifies the database connection with a simple query.
        """
        try:
            with self.engine.connect() as connection:
                result = connection.execute(text("SELECT 1"))
                if result.scalar() == 1:
                    logger.info("Database connection successful.")
                    return True
                return False
        except SQLAlchemyError as e:
            logger.error(f"Database connection failed: {e}", exc_info=True)
            return False

    def execute_query(self, query: str, params: dict = None):
        """
        Executes a SQL query and logs its performance.
        Returns results and handles errors.
        """
        start_time = time.time()
        try:
            with self.engine.connect() as connection:
                result = connection.execute(text(query), params or {})
                records = result.mappings().all()
                duration = time.time() - start_time
                self._log_query(query, params, duration)
                return records
        except SQLAlchemyError as e:
            duration = time.time() - start_time
            # KAN-475: Log detailed error, but don't expose it
            logger.error(
                f"Database query failed. Duration: {duration:.4f}s. Query: {query}. Params: {params}. Error: {e}",
                exc_info=True
            )
            # KAN-475: Return a generic error message
            raise ConnectionError("Failed to execute query due to a database error.")

    def _log_query(self, query: str, params: dict, duration: float):
        """
        Logs query details for monitoring.
        KAN-465
        """
        log_message = (
            f"Query executed. Duration: {duration:.4f}s. "
            f"Query: {query}. Params: {params}"
        )
        if duration > config.QUERY_LOG_SLOW_THRESHOLD_SEC:
            # KAN-465: Alert on slow query
            logger.warning(f"SLOW QUERY DETECTED. {log_message}")
            # Here you could integrate with a monitoring system to send an alert
        else:
            logger.info(log_message)

# Singleton instance
db_manager = DatabaseManager(config.DATABASE_URL)
