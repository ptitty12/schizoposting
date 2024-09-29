import os
from flask import Blueprint, request, render_template, jsonify
from werkzeug.utils import secure_filename
import openai
from app import db
from app.models import Note
from app.utils import allowed_file

main = Blueprint('main', __name__)


@main.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(main.root_path, '..', 'uploads', filename)
        file.save(filepath)

        # Transcribe with Whisper API
        with open(filepath, "rb") as audio_file:
            transcript = openai.Audio.transcribe("whisper-1", audio_file)

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