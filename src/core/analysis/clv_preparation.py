# KAN-484: Preparar y Validar Datos Históricos de Transacciones para CLV
import pandas as pd
import time
from src.utils.logging_config import get_logger
from src.config import config

logger = get_logger(__name__)

def prepare_clv_data(transactions_df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepares and validates historical transaction data for CLV modeling.

    Args:
        transactions_df: DataFrame with raw transaction data.
                         Expected columns: 'customer_id', 'transaction_id', 'transaction_date', 'amount'.

    Returns:
        A cleaned and normalized DataFrame ready for CLV modeling.
    """
    start_time = time.time()
    total_records = len(transactions_df)
    logger.info(f"Starting CLV data preparation for {total_records} records.")

    # 1. Handle missing critical values
    initial_nulls = transactions_df[['customer_id', 'transaction_id', 'amount']].isnull().sum().sum()
    if initial_nulls > 0:
        logger.warning(f"Found {initial_nulls} null values in critical columns. Dropping rows.")
        transactions_df.dropna(subset=['customer_id', 'transaction_id', 'amount'], inplace=True)

    # 2. Identify and report duplicates
    duplicates = transactions_df[transactions_df.duplicated(subset=['transaction_id'], keep=False)]
    if not duplicates.empty:
        logger.warning(f"Found {len(duplicates)} duplicate transaction records. Dropping duplicates.")
        # Report specific duplicate IDs
        logger.debug(f"Duplicate transaction IDs: {duplicates['transaction_id'].unique().tolist()}")
        transactions_df.drop_duplicates(subset=['transaction_id'], keep='first', inplace=True)

    # 3. Check data integrity
    final_records = len(transactions_df)
    integrity = final_records / total_records if total_records > 0 else 0
    logger.info(f"Data integrity: {integrity:.2%}")

    if integrity < config.DATA_INTEGRITY_THRESHOLD:
        # KAN-484: Alert and do not generate dataset if integrity is too low
        alert_message = f"Data integrity ({integrity:.2%}) is below the required threshold of {config.DATA_INTEGRITY_THRESHOLD:.2%}. Normalised dataset will not be generated."
        logger.error(alert_message)
        raise ValueError(alert_message)

    # 4. Normalize data (example: convert date to datetime)
    transactions_df['transaction_date'] = pd.to_datetime(transactions_df['transaction_date'])

    # 5. Check processing time
    duration_seconds = time.time() - start_time
    if duration_seconds > (config.CLV_PROCESS_TIME_LIMIT_MIN * 60):
        # KAN-484: Log performance warning
        logger.warning(f"Performance Warning: CLV data preparation took {duration_seconds:.2f}s, exceeding the {config.CLV_PROCESS_TIME_LIMIT_MIN} min limit.")

    logger.info(f"CLV data preparation completed in {duration_seconds:.2f}s. {final_records} clean records remaining.")
    return transactions_df
