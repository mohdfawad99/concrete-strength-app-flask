import os
from dotenv import load_dotenv
from flask import Flask

from app import home

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config.from_prefixed_env()

    app.register_blueprint(home.bp)

    return app