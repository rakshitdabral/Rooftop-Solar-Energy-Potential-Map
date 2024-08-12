import datetime
import os
from flask import Flask, request, jsonify, send_from_directory, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from oauthlib.oauth2 import WebApplicationClient
from io import BytesIO
import requests
from werkzeug.security import generate_password_hash, check_password_hash
from PIL import Image

app = Flask(__name__, static_folder='../frontend/build', static_url_path='/')

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app)
# CORS(app, resources={r"/api/*": {"origins": "http://127.0.0.1:3000"}})
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://aman:aman7303@localhost/solar_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

class SolarEstimation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    start_date = db.Column(db.String(8), nullable=False)
    end_date = db.Column(db.String(8), nullable=False)
    efficiency = db.Column(db.Float, nullable=False)
    annual_energy_potential = db.Column(db.Float, nullable=False)

class Polygon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    coordinates = db.Column(db.Text, nullable=False)
    image_path = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f'<Polygon {self.id}>'

@app.route('/api/signup', methods=['POST'])
def signup():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        hashed_password = generate_password_hash(data['password'])
        new_user = User(
            firstname=data['firstname'],
            lastname=data['lastname'],
            email=data['email'],
            password=hashed_password
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User created successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        user = User.query.filter_by(email=data['email']).first()
        if user and check_password_hash(user.password, data['password']):
            return jsonify({"message": "Login successful", "user_id": user.id}), 200
        return jsonify({"error": "Invalid credentials"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/estimate', methods=['POST'])
def estimate():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        response = requests.get('https://power.larc.nasa.gov/api/temporal/daily/point', params={
            'parameters': 'ALLSKY_SFC_SW_DWN',
            'community': 'RE',
            'longitude': data['longitude'],
            'latitude': data['latitude'],
            'start': data['startDate'],
            'end': data['endDate'],
            'format': 'json',
        })
        
        if response.status_code != 200:
            return jsonify({"error": "Failed to fetch solar data"}), 500
        
        solar_data = response.json()['properties']['parameter']['ALLSKY_SFC_SW_DWN']
        
        annual_energy_potential = sum(solar_data.values()) * 500 * float(data['efficiency'])
        
        new_estimation = SolarEstimation(
            user_id=data['user_id'],
            latitude=data['latitude'],
            longitude=data['longitude'],
            start_date=data['startDate'],
            end_date=data['endDate'],
            efficiency=data['efficiency'],
            annual_energy_potential=annual_energy_potential
        )
        db.session.add(new_estimation)
        db.session.commit()
        
        return jsonify({"solar_data": solar_data, "annual_energy_potential": annual_energy_potential}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/api/save_image', methods=['POST'])
def save_image():
    try:
        data = request.get_json()
        image_url = data['imageUrl']
        user_id = data['user_id']
        
        response = requests.get(image_url)
        image = Image.open(BytesIO(response.content))
        
        image_path = os.path.join(UPLOAD_FOLDER, f'{user_id}_satellite_image.png')
        image.save(image_path)
        
        return jsonify({'message': 'Image saved successfully', 'imagePath': image_path})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/save_polygon', methods=['POST'])
def save_polygon():
    try:
        data = request.get_json()
        coordinates = data['coordinates']
        image_url = data['imageUrl']
        user_id = data['user_id']
        
        # Download the image from the URL
        response = requests.get(image_url)
        response.raise_for_status()
        
        # Open the image using PIL
        image = Image.open(BytesIO(response.content))
        
        # Save the image locally
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], f'{user_id}_polygon_image.png')
        image.save(image_path)
        
        
        return jsonify({'message': 'Polygon image saved successfully', 'imagePath': image_path})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Serve React App
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_react_app(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)





    


