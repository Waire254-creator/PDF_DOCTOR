from flask import Blueprint, render_template, request, redirect, url_for, send_from_directory, current_app, flash
from werkzeug.utils import secure_filename
import os


bp = Blueprint('main', __name__)

@bp.route('/')
def home():
    return render_template('home.html')

