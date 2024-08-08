import os
from flask import Flask


app = Flask(__name__)

UPLOAD_FOLDER = 'temp/uploads'
MERGED_FOLDER = 'C:\\Users\\Admin\\Documents\\PDF_DOCTOR\\temp/merged\\'
ORGANIZED_FOLDER = 'C:\\Users\\Admin\\Documents\\PDF_DOCTOR\\temp/organized\\'
ROTATED_FOLDER = 'C:\\Users\\Admin\\Documents\\PDF_DOCTOR\\temp/rotated\\'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(MERGED_FOLDER, exist_ok=True)
os.makedirs(ORGANIZED_FOLDER, exist_ok=True)
os.makedirs(ROTATED_FOLDER, exist_ok=True)

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///users.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False