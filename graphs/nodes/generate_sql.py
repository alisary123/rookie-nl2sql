"""
SQL generation node for LangGraph.
M0: Placeholder implementation that returns a simple response.
"""
from typing import Dict, Any
from datetime import datetime
from graphs.state import NL2SQLState


def generate_sql_node(state: NL2SQLState) -> Dict[str, Any]:
    """
    Generate SQL from user query (M0: placeholder implementation).
    
    Args:
        state: Current workflow state
        
    Returns:
        Updated state with SQL generation info
    """
    # M0: Simple implementation - just return the original query
    question = state.get("question", "")
    sql_response = f"Processed query: '{question}'"
    
    return {
        **state,
        "candidate_sql": sql_response,  # Use candidate_sql for consistency
        "sql_generated_at": str(datetime.now())
    }