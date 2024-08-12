"""
hacked namespace uses `__all__` as a whitelist of symbols which are executable source code.
Non-whitelisted modules or runtime constituents are treated as 'data' which we call associative 
'articles' within the knowledge base, loaded at runtime.
"""
import importlib.util
from pathlib import Path
from types import SimpleNamespace
# __all__ needs to do more than specify wildcard imports, it needs to WHITELIST source code/libs
def initialize_kb(base_dir):
    """Initialize the knowledge base from a given base directory."""
    kb_globals = SimpleNamespace()
    kb_globals.__all__ = []

    base_dir = Path(base_dir) if not isinstance(base_dir, Path) else base_dir

    def dynamic_import_py_modules(directory):
        """Dynamically import Python modules and update __all__."""
        for path in directory.rglob("*.py"):
            if path.name.startswith("_") or path.name == "main.py":
                continue
            try:
                module_name = path.stem
                spec = importlib.util.spec_from_file_location(module_name, str(path))
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                setattr(kb_globals, module_name, module)
                kb_globals.__all__.append(module_name)
            except Exception as e:
                print(f"Error importing module {module_name}: {e}")

    def load_articles(directory):
        """Load text articles (e.g., .md, .txt) into the knowledge base namespace."""
        for suffix in ['*.md', '*.txt']:
            for path in directory.rglob(suffix):
                try:
                    article_name = path.stem
                    content = path.read_text()
                    article = SimpleNamespace(
                        content=content,
                        path=str(path)
                    )
                    setattr(kb_globals, article_name, article)
                except Exception as e:
                    print(f"Error loading article from {path}: {e}")

    dynamic_import_py_modules(base_dir)
    load_articles(base_dir)
    
    return kb_globals