# KAN-473: Generar Consultas SQL Parametrizadas
from typing import Dict, Any, Tuple

class QueryBuilder:
    """
    Builds safe, parameterized SQL queries from structured parameters.
    """

    def build(self, parsed_query: Dict[str, Any]) -> Tuple[str, Dict]:
        """
        Constructs a SQL query string and its parameters.

        Args:
            parsed_query: A dictionary with structured query parameters from IntentParser.

        Returns:
            A tuple containing the SQL query string and a dictionary of parameters.
        """
        table = parsed_query["table"]
        fields = ", ".join(parsed_query["fields"])
        
        query = f"SELECT {fields} FROM {table}"
        
        params = {}
        
        conditions = parsed_query.get("conditions", [])
        if conditions:
            where_clauses = []
            for i, cond in enumerate(conditions):
                param_name = f"param_{i}"
                # Handle IN clauses for lists of values
                if isinstance(cond['value'], list):
                    in_params = []
                    for j, val in enumerate(cond['value']):
                        in_param_name = f"{param_name}_{j}"
                        in_params.append(f":{in_param_name}")
                        params[in_param_name] = val
                    where_clauses.append(f"{cond['field']} IN ({', '.join(in_params)})")
                else:
                    # KAN-473: Use named parameters to prevent SQL injection
                    where_clauses.append(f"{cond['field']} {cond['operator']} :{param_name}")
                    params[param_name] = cond['value']
            
            query += " WHERE " + " AND ".join(where_clauses)

        group_by = parsed_query.get("group_by")
        if group_by:
            query += f" GROUP BY {', '.join(group_by)}"

        order_by = parsed_query.get("order_by")
        if order_by:
            # Assuming order_by is a list of dicts like [{"field": "name", "direction": "ASC"}]
            order_clauses = [f"{o['field']} {o.get('direction', 'ASC')}" for o in order_by]
            query += f" ORDER BY {', '.join(order_clauses)}"

        limit = parsed_query.get("limit")
        if limit:
            query += " LIMIT :limit"
            params["limit"] = limit

        # KAN-473: Ensure no direct string interpolation of user values
        # All values are handled by the parameter dictionary.
        return query, params

# Singleton instance
query_builder = QueryBuilder()
