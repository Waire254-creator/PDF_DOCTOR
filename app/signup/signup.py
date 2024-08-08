from flask import Flask, request, jsonify, render_template, Blueprint
from flask_sqlalchemy import SQLAlchemy
import re
from config import Config
from app.models import User, db
signup_bp=Blueprint('signup', __name__)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Import the User model here

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    
    with app.app_context():
        db.create_all()

@signup_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    
    if request.method == 'POST':
        data = request.json
        
        # Validate username (alphanumeric and underscore only)
        if not re.match(r'^\w+$', data['username']):
            return jsonify({"success": False, "message": "Invalid username format"}), 400
        
        # Validate email
        if not re.match(r'[^@]+@[^@]+\.[^@]+', data['email']):
            return jsonify({"success": False, "message": "Invalid email format"}), 400
        
        # Validate phone number (simple check, adjust as needed)
        if not data['phonenumber'].isdigit():
            return jsonify({"success": False, "message": "Invalid phone number"}), 400
        
        # Check if username or email already exists
        if User.query.filter_by(username=data['username']).first():
            return jsonify({"success": False, "message": "Username already exists"}), 400
        if User.query.filter_by(email=data['email']).first():
            return jsonify({"success": False, "message": "Email already exists"}), 400
        
        # Create new user
        new_user = User(
            username=data['username'],
            firstname=data['firstname'],
            lastname=data['lastname'],
            email=data['email'],
            country_code=data['countryCode'],
            phone_number=data['phonenumber']
        )
        new_user.set_password(data['password'])
        
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({"success": True, "message": "User created successfully"}), 201
    return app
if __name__ == '__main__':
    app.run(debug=True)