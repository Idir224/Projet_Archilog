from flask import Flask
from archilog.config import config
from archilog.views import gui, cli  # Si tu ajoutes API plus tard, ajoute-le ici

def create_app():
    app = Flask(__name__)
    app.config.from_prefixed_env(prefix="ARCHILOG_FLASK")
    app.register_blueprint(gui.web_ui, url_prefix="/")
    return app
