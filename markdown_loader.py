import os
from types import SimpleNamespace
import markdown

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