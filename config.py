import os

class Config:
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY') or 'fallback-key-for-development'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB limit
    OPENAI_API_KEY = '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'