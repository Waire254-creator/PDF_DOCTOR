from flask import Flask, Blueprint, request, render_template, jsonify, send_file, current_app
from werkzeug.utils import secure_filename
import os
import uuid
from PyPDF2 import PdfReader, PdfWriter
import json
from config import app

organize_bp = Blueprint('organize', __name__, template_folder='templates')

UPLOAD_FOLDER = 'temp/uploads'
ORGANIZED_FOLDER = 'C:\\Users\\Admin\\Documents\\PDF_DOCTOR\\temp/organized\\'
ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@organize_bp.route('/organize_pdf', methods=['GET'])
def index():
    return render_template('organize/organize.html')

@organize_bp.route('/organize', methods=['POST'])
def organize():
    if 'pdf' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['pdf']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

        pages_data = json.loads(request.form['pages'])
        
        reader = PdfReader(file_path)
        writer = PdfWriter()

        for page_info in pages_data:
            page = reader.pages[page_info['index']]
            if page_info['rotation'] != 0:
                page.rotate(page_info['rotation'])
            writer.add_page(page)

        # Use the provided filename or generate a unique one
        if 'filename' in request.form and request.form['filename'].strip():
            organized_filename = secure_filename(request.form['filename'])
            if not organized_filename.lower().endswith('.pdf'):
                organized_filename += '.pdf'
        else:
            organized_filename = f"{uuid.uuid4()}.pdf"
        
        organized_file_path = os.path.join(ORGANIZED_FOLDER, organized_filename)
        
        with open(organized_file_path, 'wb') as output_file:
            writer.write(output_file)

        os.remove(file_path)  # Remove the original uploaded file

        return jsonify({'filename': organized_filename}), 200
    
    return jsonify({'error': 'Invalid file type'}), 400

@organize_bp.route('/organize/download/<filename>', methods=['GET'])
def download_page(filename):
    return render_template('organize/download.html', filename=filename)

@organize_bp.route('/organized/download_file/<filename>', methods=['GET'])
def download_file(filename):
    return send_file(os.path.join(ORGANIZED_FOLDER, filename), as_attachment=True)



if __name__ == '__main__':
    app.run(debug=True)