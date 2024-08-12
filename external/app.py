import os
from types import SimpleNamespace
import markdown
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

def load_markdown_files(directory):
    knowledge_base = SimpleNamespace()
    for filename in os.listdir(directory):
        if filename.endswith('.md'):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r') as file:
                content = file.read()
                html_content = markdown.markdown(content)
                setattr(knowledge_base, filename[:-3], SimpleNamespace(content=content, html=html_content))
    return knowledge_base