from flask import Flask, render_template, request, send_file, Blueprint, jsonify, url_for
from PyPDF2 import PdfWriter, PdfReader
import os
import io
import uuid
import logging
from config import app

app = Flask(__name__)

merge_bp = Blueprint('merge', __name__)

logging.basicConfig(level=logging.DEBUG)
UPLOAD_FOLDER = 'temp/uploads'
MERGED_FOLDER = 'C:\\Users\\Admin\\Documents\\PDF_DOCTOR\\temp/merged\\'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(MERGED_FOLDER, exist_ok=True)

@merge_bp.route('/merge_pdf')
def index():
    return render_template('merge/merge.html')

ALLOWED_EXTENSIONS = {'pdf'}

def parse_page_range(range_string, max_pages):
    pages = set()
    for part in range_string.split(','):
        part = part.strip()
        if '-' in part:
            start, end = map(int, part.split('-'))
            pages.update(range(max(1, start), min(end + 1, max_pages + 1)))
        elif part.lower() == 'all':
            pages.update(range(1, max_pages + 1))
        else:
            try:
                page = int(part)
                if 1 <= page <= max_pages:
                    pages.add(page)
            except ValueError:
                pass  # ignore non-integer inputs
    return sorted(list(pages))


@merge_bp.route('/merge', methods=['POST'])
def merge_pdfs():
    try:
        if 'files[]' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        
        files = request.files.getlist('files[]')
        page_ranges = request.form.getlist('pageRanges[]')
        output_filename = request.form.get('outputFilename', 'merged.pdf')
        
        unique_id = str(uuid.uuid4())
        
        if not output_filename.lower().endswith('.pdf'):
            output_filename += '.pdf'
        
        unique_filename = f"{unique_id}_{output_filename}"
        
        merger = PdfWriter()

        for file, page_range in zip(files, page_ranges):
            pdf = PdfReader(file)
            pages = parse_page_range(page_range, len(pdf.pages))
            
            for page_num in pages:
                if 0 < page_num <= len(pdf.pages):
                    merger.add_page(pdf.pages[page_num - 1])

        temp_file_path = os.path.join('C:\\Users\\Admin\\Documents\\PDF_DOCTOR\\temp/merged\\', unique_filename)
        with open(temp_file_path, 'wb') as temp_file:
            merger.write(temp_file)

        download_url = url_for('merge.download_file', filename=unique_filename)
        download_page_url = url_for('merge.download_page', filename=unique_filename)

        app.logger.info(f"PDF merged successfully. Filename: {output_filename}, Unique filename: {unique_filename}")

        return jsonify({
            'status': 'success', 
            'filename': output_filename,
            'unique_filename': unique_filename,
            'download_url': download_url,
            'download_page_url': download_page_url
        })

    except Exception as e:
        app.logger.error(f"Error during PDF merge: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500



@merge_bp.route('/download/<filename>')
def download_file(filename):
    try:
        file_path = os.path.join(MERGED_FOLDER, filename)
        if not os.path.exists(file_path):
            app.logger.error(f"File not found: {file_path}")
            return "File not found", 404
        
        original_filename = "_".join(filename.split("_")[1:])
        
        app.logger.info(f"Sending file: {original_filename}")
        return send_file(file_path, as_attachment=True, download_name=original_filename)
    except Exception as e:
        app.logger.error(f"Error during file download: {str(e)}")
        return "Error downloading file", 500

@merge_bp.route('/download')
def download_page():
    filename = request.args.get('filename', 'merged.pdf')
    download_url = url_for('merge.download_file', filename=filename, _external=True)
    return render_template('merge/download.html', filename=filename, download_url=download_url)


if __name__ == '__main__':
    app.run(debug=True)
    