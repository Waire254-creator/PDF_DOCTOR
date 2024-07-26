from flask import jsonify
from PyPDF2 import PdfReader, PdfWriter
import os
import tempfile

def upload_pdf(file):
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file and file.filename.endswith('.pdf'):
        temp_dir = tempfile.mkdtemp(dir='temp')
        temp_path = os.path.join(temp_dir, 'original.pdf')
        file.save(temp_path)
        return jsonify({"message": "File uploaded successfully", "path": temp_path}), 200
    return jsonify({"error": "Invalid file type"}), 400

def reorganize_pdf(original_path, new_order):
    reader = PdfReader(original_path)
    writer = PdfWriter()

    for i in new_order:
        writer.add_page(reader.pages[i])

    output_path = os.path.join(os.path.dirname(original_path), 'reorganized.pdf')
    with open(output_path, 'wb') as output_file:
        writer.write(output_file)

    return jsonify({"message": "PDF reorganized successfully", "path": output_path}), 200

def rotate_page(original_path, page_number, rotation):
    reader = PdfReader(original_path)
    writer = PdfWriter()

    for i, page in enumerate(reader.pages):
        if i == page_number:
            page.rotate(rotation)
        writer.add_page(page)

    output_path = os.path.join(os.path.dirname(original_path), 'rotated.pdf')
    with open(output_path, 'wb') as output_file:
        writer.write(output_file)

    return jsonify({"message": "Page rotated successfully", "path": output_path}), 200

def add_blank_page(original_path, after_page):
    reader = PdfReader(original_path)
    writer = PdfWriter()

    for i, page in enumerate(reader.pages):
        writer.add_page(page)
        if i == after_page:
            writer.add_blank_page()

    output_path = os.path.join(os.path.dirname(original_path), 'with_blank_page.pdf')
    with open(output_path, 'wb') as output_file:
        writer.write(output_file)

    return jsonify({"message": "Blank page added successfully", "path": output_path}), 200