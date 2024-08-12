# Assume __init__.py sets 'kb' in the global namespace
import os
import ast
import logging
from __init__ import initialize_kb

logger = logging.getLogger(__name__)

current_directory = os.getcwd()
kb = initialize_kb(current_directory)

def execute_repl_query(query, knowledge_base):
    try:
        parsed = ast.parse(query, mode='eval')
        result = eval(compile(parsed, '<string>', 'eval'), {'kb': knowledge_base})
        return str(result)
    except Exception as e:
        logger.error(f"Error executing REPL query: {e}")
        return f"Error: {str(e)}"

def repl():
    print("Enter 'exit' or 'quit' to leave the REPL.")
    while True:
        try:
            query = input(">>> ")
            if query.lower() in {'exit', 'quit'}:
                break
            result = execute_repl_query(query, kb)
            print(result)
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    print("Running Knowledge Base Application REPL in:", current_directory)
    repl()
