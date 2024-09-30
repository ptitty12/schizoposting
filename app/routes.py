import os
from flask import Blueprint, request, render_template, jsonify
from werkzeug.utils import secure_filename
from openai import OpenAI
from flask import current_app as app
from app import db
from app.models import Note
from app.utils import allowed_file
from flask_cors import CORS


main = Blueprint('main', __name__)
CORS(main)

from flask import current_app
from werkzeug.exceptions import RequestEntityTooLarge

import io
from werkzeug.datastructures import FileStorage



import whisper

# Load the model once when the application starts
model = whisper.load_model("base")

@main.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        if file and allowed_file(file.filename):
            # Save the file temporarily
            temp_path = os.path.join('/tmp', file.filename)
            file.save(temp_path)

            # Transcribe the audio
            result = model.transcribe(temp_path)

            # Remove the temporary file
            os.remove(temp_path)

            # Save transcription to database
            new_note = Note(content=result["text"])
            db.session.add(new_note)
            db.session.commit()

            return jsonify({'message': 'File uploaded and transcribed successfully'}), 200
        else:
            return jsonify({'error': 'File type not allowed'}), 400

    except Exception as e:
        current_app.logger.error(f'Error processing upload: {str(e)}')
        return jsonify({'error': 'Internal server error'}), 500


@main.route('/')
def index():
    notes = Note.query.order_by(Note.date.desc()).all()
    return render_template('index.html', notes=notes)