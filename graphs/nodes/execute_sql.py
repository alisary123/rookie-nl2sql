"""
SQL execution node for LangGraph.
M0: Placeholder implementation - no actual execution.
"""
from typing import Dict, Any
from datetime import datetime
from graphs.state import NL2SQLState


def execute_sql_node(state: NL2SQLState) -> Dict[str, Any]:
    """
    Execute SQL query (M0: placeholder implementation).
    
    Args:
        state: Current workflow state
        
    Returns:
        Updated state with execution results
    """
    # M0: Simple implementation - no actual SQL execution
    sql_query = state.get('candidate_sql', 'N/A')
    result = f"M0 placeholder - no actual execution for: {sql_query}"
    
    # Return execution_result as dictionary for consistency
    execution_result = {
        "ok": True,  # M0: always succeed
        "message": result,
        "row_count": 0,
        "columns": [],
        "rows": []
    }
    
    return {
        **state,
        "execution_result": execution_result,
        "executed_at": str(datetime.now())
    }