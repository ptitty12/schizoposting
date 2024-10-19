import os
from flask import Blueprint, request, render_template, jsonify, current_app
from werkzeug.utils import secure_filename
from openai import OpenAI
from app import db
from app.models import Note
from app.utils import allowed_file
from flask_cors import CORS
import io

main = Blueprint('main', __name__)
CORS(main)

def get_openai_client():
    return OpenAI(api_key=current_app.config['OPENAI_API_KEY'])

@main.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        if file and allowed_file(file.filename):
            # Read the file data
            file_data = file.read()

            # Create a file-like object
            file_object = io.BytesIO(file_data)
            file_object.name = file.filename  # Add a name attribute

            # Get the OpenAI client
            client = get_openai_client()

            # Get the IP address of the submitter
            submitter_ip = request.remote_addr

            # Transcribe with Whisper API
            transcript = client.audio.transcriptions.create(
                file=file_object,
                model="whisper-1",
                response_format="text",
                language="en"
            )

            # Generate summary using ChatGPT
            chat_completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that summarizes my random thoughts in a few words."},
                    {"role": "user", "content": f"Summarize this text in 5 words or less: {transcript}"}
                ]
            )
            summary = chat_completion.choices[0].message.content.strip()

            # Save transcription and summary to database with IP address
            new_note = Note(content=transcript, summary=summary, ip_address=submitter_ip)
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
