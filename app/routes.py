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


@main.route('/upload', methods=['POST'])
def upload_file():
    app.logger.info('Upload endpoint hit with method: %s', request.method)

    if 'file' not in request.files:
        app.logger.error('No file part in request')
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        app.logger.error('No selected file')
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(main.root_path, '..', 'uploads', filename)
        file.save(filepath)

        app.logger.info(f'File {filename} saved successfully')

        # Transcribe with Whisper API
        try:
            with open(filepath, "rb") as audio_file:
                transcript = openai.Audio.transcribe("whisper-1", audio_file)
        except Exception as e:
            app.logger.error(f'Error during transcription: {e}')
            return jsonify({'error': 'Transcription failed'}), 500

        # Save transcription to database
        new_note = Note(content=transcript['text'])
        db.session.add(new_note)
        db.session.commit()

        # Clean up the uploaded file
        os.remove(filepath)

        return jsonify({'message': 'File uploaded and transcribed successfully'}), 200


@main.route('/')
def index():
    notes = Note.query.order_by(Note.date.desc()).all()
    return render_template('index.html', notes=notes)