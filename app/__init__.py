from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
import openai
import os

db = SQLAlchemy()
migrate = Migrate()
def create_app():
    app = Flask(__name__, template_folder=os.path.abspath('templates'))
    app.config.from_object(Config)
    app.config['MAX_CONTENT_LENGTH'] = 55 * 1024 * 1024  # 16 MB limit
    db.init_app(app)
    migrate.init_app(app, db)

    # Set OpenAI API key
    openai.api_key = app.config['OPENAI_API_KEY']

    from app import routes
    app.register_blueprint(routes.main)

    with app.app_context():
        db.create_all()

    return app