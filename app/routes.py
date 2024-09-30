import os
from flask import Blueprint, request, render_template, jsonify
from werkzeug.utils import secure_filename
import openai
from flask import current_app as app
from app import db
from app.models import Note
from app.utils import allowed_file
from flask_cors import CORS


main = Blueprint('main', __name__)
CORS(main)

from flask import current_app
from werkzeug.exceptions import RequestEntityTooLarge


@main.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        if file and allowed_file(file.filename):
            # Process file in memory
            audio_data = file.read()

            # Transcribe with Whisper API
            transcript = openai.Audio.transcribe("whisper-1", audio_data)

            # Save transcription to database
            new_note = Note(content=transcript['text'])
            db.session.add(new_note)
            db.session.commit()

            return jsonify({'message': 'File uploaded and transcribed successfully'}), 200
        else:
            return jsonify({'error': 'File type not allowed'}), 400

    except RequestEntityTooLarge:
        return jsonify({'error': 'File too large'}), 413
    except Exception as e:
        current_app.logger.error(f'Error processing upload: {str(e)}')
        return jsonify({'error': 'Internal server error'}), 500


@main.route('/')
def index():
    notes = Note.query.order_by(Note.date.desc()).all()
    return render_template('index.html', notes=notes)