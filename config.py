import os

class Config:
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY') or 'fallback-key-for-development'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB limit
    my_key_1 = 'sk-proj-u5fLSdRphFLjigYJ8gls'
    my_key_2 = 'QOafHrkodnUbiCNf2DkPYi3BW7z7FrZUH0Dgqw9DxxxIk5ZJj7qJnmT3BlbkFJ__kKgMoIi40DSSOlndk8jRb6arLlKXgjb7GPlfvfvuwxDxtI7jQBozm2w4bYAO7mvEl-5HNicA'
    OPENAI_API_KEY = my_key_1+my_key_2