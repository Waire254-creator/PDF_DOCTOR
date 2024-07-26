from flask import Flask, request, jsonify, send_file, render_template
from app.organize import bp
from app.organize.utils import upload_pdf, reorganize_pdf, rotate_page, add_blank_page
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = 'temp'
ALLOWED_EXTENSIONS = {'pdf'}
app = Flask(__name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/')
def index():
    return render_template('organize/organize.html')

@bp.route('/', methods=['GET', 'POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    return upload_pdf(file)

@bp.route('/reorganize', methods=['POST'])
def reorganize():
    data = request.json
    return reorganize_pdf(data['path'], data['order'])

@bp.route('/rotate', methods=['POST'])
def rotate():
    data = request.json
    return rotate_page(data['path'], data['pageNumber'], data['rotation'])

@bp.route('/add-blank-page', methods=['POST'])
def add_blank():
    data = request.json
    return add_blank_page(data['path'], data['afterPage'])

@bp.route('/download/<path:filename>')
def download_file(filename):
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)