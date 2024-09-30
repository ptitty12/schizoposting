import os

class Config:
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY') or 'fallback-key-for-development'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB limit
    my_key_1 = 'sk-proj-28wh3-gKOSLWt-HFki88uK3Tcf6Zunb1s1iOdk9RzpUNA3waBApzLsdVd4thMIb7'
    my_key_2 = 'VVRQsZ6fsdT3BlbkFJcCpWfIs3X7Kqd79op7heOsAZ_BPBbJ71hMwBtSlarQ9zHJ4HoEXEe_hEfjHCtKKxigv2SGlyQA'
    OPENAI_API_KEY = my_key_1+my_key_2