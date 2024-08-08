from flask import Flask


def create_app():
    app = Flask(__name__)
    

    from .routes import bp as main_bp
    app.register_blueprint(main_bp)

    from .merge.utils import merge_bp
    app.register_blueprint(merge_bp)
    

    from .split.routes import bp as split_bp
    app.register_blueprint(split_bp)

    from .organize.utils import organize_bp
    app.register_blueprint(organize_bp)

    from .repair.routes import bp as repair_bp
    app.register_blueprint(repair_bp)
    
    from .rotate.utils import rotate_bp
    app.register_blueprint(rotate_bp)

    from .signup.signup import signup_bp
    app.register_blueprint(signup_bp)


    return app