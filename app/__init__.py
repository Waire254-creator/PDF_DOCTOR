from flask import Flask 
from flask import render_template, request, jsonify, send_file
from config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)


    #from app.merge import bp as merge_bp
    #app.register_blueprint(merge_bp, url_prefix='/merge')
    from app.organize import bp as organize_bp
    app.register_blueprint(organize_bp, url_prefix='/organize_pdf')


    app.secret_key = 'Waire254'
    from app.main.views import main_bp
    app.register_blueprint(main_bp, url_prefix='/')

    @app.route('/')
    def base():
        return render_template('base.html')

    return app