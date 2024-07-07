import logging
import os
from flask import Flask, render_template, request, jsonify
from gunicorn.app.base import BaseApplication
from src.utils.loader import load_markdown_files, execute_repl_query

def create_app():
    app = Flask(__name__, static_folder='static')

    @app.route("/")
    def home_route():
        return render_template("home.html")

    return app

app = create_app()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load markdown files
kb_dir = os.path.join(os.path.dirname(__file__), 'kb')
if not os.path.exists(kb_dir):
    os.makedirs(kb_dir)
    logger.info(f"Created directory: {kb_dir}")
knowledge_base = load_markdown_files(kb_dir)

@app.route('/repl', methods=['POST'])
def repl():
    query = request.json.get('query')
    result = execute_repl_query(query, knowledge_base)
    return jsonify({'result': result})

class StandaloneApplication(BaseApplication):
    def __init__(self, app, options=None):
        self.application = app
        self.options = options or {}
        super().__init__()

    def load_config(self):
        # Apply configuration to Gunicorn
        for key, value in self.options.items():
            if key in self.cfg.settings and value is not None:
                self.cfg.set(key.lower(), value)

    def load(self):
        return self.application

if __name__ == "__main__":
    options = {
        "bind": "0.0.0.0:8080",
        "workers": 4,
        "loglevel": "info",
        "accesslog": "-"
    }
    StandaloneApplication(app, options).run()