from flask import Flask
from archilog.views.gui import web_ui
from archilog.config import config

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = config.DATABASE_URL
    app.config["DEBUG"] = config.DEBUG

    app.register_blueprint(web_ui, url_prefix="/")

    return app