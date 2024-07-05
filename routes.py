from flask import render_template, Flask

def create_app():
    app = Flask(__name__, static_folder='static')

    @app.route("/")
    def home_route():
        return render_template("home.html")

    return app