import ast
import logging

logger = logging.getLogger(__name__)

def execute_repl_query(query, knowledge_base):
    try:
        # Parse the query as a Python expression
        parsed = ast.parse(query, mode='eval')
        
        # Evaluate the expression in a restricted environment
        result = eval(compile(parsed, '<string>', 'eval'), {'kb': knowledge_base})
        
        # Convert the result to a string representation
        return str(result)
    except Exception as e:
        logger.error(f"Error executing REPL query: {e}")
        return f"Error: {str(e)}"