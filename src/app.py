from flask import Flask
from src.routes import product_bp


def create_app():
    app = Flask(__name__)
    app.register_blueprint(product_bp)

    return app
