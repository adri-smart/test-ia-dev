# KAN-480, KAN-481, KAN-482, KAN-483: Customer Segmentation Logic
import pandas as pd
import time
from src.utils.logging_config import get_logger
from src.config import config

logger = get_logger(__name__)

def segment_customers(customers_df: pd.DataFrame, criteria: dict) -> pd.DataFrame:
    """
    Segments customers based on specific criteria.
    KAN-480
    """
    start_time = time.time()
    logger.info(f"Starting basic segmentation for {len(customers_df)} customers.")
    
    # Example criteria: {"age_min": 18, "age_max": 35, "location": "Madrid"}
    query_parts = []
    if 'age_min' in criteria:
        query_parts.append(f"age >= {criteria['age_min']}")
    if 'age_max' in criteria:
        query_parts.append(f"age <= {criteria['age_max']}")
    if 'location' in criteria:
        query_parts.append(f"ubicacion == '{criteria['location']}'")
    
    query = " & ".join(query_parts)
    segmented_df = customers_df.query(query)
    
    # Assign segment label
    segment_label = criteria.get("label", "custom_segment")
    segmented_df['segment'] = segment_label
    
    duration = time.time() - start_time
    if duration > config.SEGMENTATION_TIME_LIMIT_SEC:
        logger.warning(f"Segmentation took {duration:.2f}s, exceeding the {config.SEGMENTATION_TIME_LIMIT_SEC}s limit.")
    
    logger.info(f"Segmentation complete. Found {len(segmented_df)} customers in segment '{segment_label}'.")
    return segmented_df

def calculate_segment_metrics(segmented_df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates aggregated metrics for each segment.
    KAN-481
    """
    if 'segment' not in segmented_df.columns:
        raise ValueError("Input DataFrame must have a 'segment' column.")
        
    logger.info("Calculating metrics for segments.")
    
    # Assuming df has columns: segment, client_id, total_spent, is_retained
    # Ensure required columns exist, filling with defaults if not
    for col in ['total_spent', 'is_retained']:
        if col not in segmented_df:
            segmented_df[col] = 0 if col == 'total_spent' else False

    metrics = segmented_df.groupby('segment').agg(
        cantidad_clientes=('client_id', 'nunique'),
        ingresos_totales=('total_spent', 'sum'),
        tasa_retencion=('is_retained', lambda x: x.mean() * 100)
    ).reset_index()
    
    metrics['ticket_promedio'] = metrics['ingresos_totales'] / metrics['cantidad_clientes']
    metrics['ticket_promedio'] = metrics['ticket_promedio'].fillna(0)
    
    logger.info(f"Calculated metrics for {len(metrics)} segments.")
    return metrics

def get_segment_drilldown(customers_df: pd.DataFrame, segment_name: str, page: int = 1, page_size: int = 50) -> pd.DataFrame:
    """
    Provides a paginated list of customers within a specific segment.
    KAN-482
    """
    start_time = time.time()
    segment_customers = customers_df[customers_df['segment'] == segment_name]
    
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    
    paginated_customers = segment_customers.iloc[start_index:end_index]
    
    duration = time.time() - start_time
    if duration > config.DRILL_DOWN_TIME_LIMIT_SEC:
        logger.warning(f"Drill-down took {duration:.2f}s, exceeding the {config.DRILL_DOWN_TIME_LIMIT_SEC}s limit.")
        
    return paginated_customers

def filter_by_purchase_behavior(purchases_df: pd.DataFrame, product_a: str, product_b: str) -> list:
    """
    Filters for customers who bought product A but not product B.
    KAN-483
    
    Args:
        purchases_df: DataFrame with 'cliente_id' and 'producto_comprado'
        product_a: The product that must have been purchased.
        product_b: The product that must NOT have been purchased.
    """
    logger.info(f"Filtering for customers who bought '{product_a}' but not '{product_b}'.")
    
    bought_a = set(purchases_df[purchases_df['producto_comprado'] == product_a]['cliente_id'])
    bought_b = set(purchases_df[purchases_df['producto_comprado'] == product_b]['cliente_id'])
    
    result_customers = list(bought_a - bought_b)
    
    if not result_customers:
        logger.info("No customers found matching the criteria.")
        return []
        
    logger.info(f"Found {len(result_customers)} customers matching the criteria.")
    return result_customers
