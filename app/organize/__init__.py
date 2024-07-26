from flask import Blueprint

bp = Blueprint('organize', __name__)

from app.organize import routes