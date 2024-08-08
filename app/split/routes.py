from flask import Blueprint, render_template, request, send_file, jsonify
import os
from PyPDF2 import PdfFileMerger
from pdf2image import convert_from_path
from werkzeug.utils import secure_filename

bp = Blueprint('split', __name__)

UPLOAD_FOLDER = 'temp/uploads'
PROCESSED_FOLDER = 'temp/processed'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(PROCESSED_FOLDER):
    os.makedirs(PROCESSED_FOLDER)