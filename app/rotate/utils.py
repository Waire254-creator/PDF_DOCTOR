from flask import Flask, request, jsonify, send_file, render_template, Blueprint
from werkzeug.utils import secure_filename
import os
import uuid
from PyPDF2 import PdfReader, PdfWriter
import json

app = Flask(__name__)
rotate_bp = Blueprint('rotate', __name__)
UPLOAD_FOLDER = 'temp/uploads'
ROTATED_FOLDER = 'C:\\Users\\Admin\\Documents\\PDF_DOCTOR\\temp/rotated\\'
ALLOWED_EXTENSIONS = {'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ROTATED_FOLDER'] = ROTATED_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@rotate_bp.route('/rotate_pdf', methods=['GET'])
def index():
    return render_template('rotate/rotate.html')

@rotate_bp.route('/rotate/upload', methods=['POST'])
def rotate_upload_file():
    if 'pdf' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['pdf']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        return jsonify({'filename': filename}), 200
    
    return jsonify({'error': 'Invalid file type'}), 400

@rotate_bp.route('/rotate', methods=['POST'])
def rotate_pdf():
    data = request.json
    filename = data['filename']
    pages_data = data['pages']  # Expect an array of objects with 'index' and 'rotation'
    
    input_path = os.path.join(UPLOAD_FOLDER, filename)
    output_filename = f"rotated_{uuid.uuid4()}.pdf"
    output_path = os.path.join(ROTATED_FOLDER, output_filename)
    
    reader = PdfReader(input_path)
    writer = PdfWriter()
    
    for page_info in pages_data:
        page = reader.pages[page_info['index']]
        if page_info['rotation'] != 0:
            page.rotate(page_info['rotation'])
        writer.add_page(page)
    
    with open(output_path, 'wb') as output_file:
        writer.write(output_file)
    
    os.remove(input_path)  # Remove the original uploaded file
    
    return jsonify({'rotated_filename': output_filename}), 200

@rotate_bp.route('/rotate/download/<filename>', methods=['GET'])
def rotated_download_page(filename):
    return render_template('rotate/download.html')

@rotate_bp.route('/rotated/download/<filename>', methods=['GET'])
def download_file(filename):
    return send_file(os.path.join(ROTATED_FOLDER, filename), as_attachment=True)

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(ROTATED_FOLDER, exist_ok=True)
    app.run(debug=True)