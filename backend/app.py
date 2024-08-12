import datetime
import logging
import os
import sys

import pandas as pd
import psycopg2
import requests
from flask import Flask, jsonify, render_template, request, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from shapely.geometry import Polygon
from shapely.geometry.polygon import orient
from werkzeug.utils import secure_filename

from model.solar_potential import calculate_solar_potential

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://aman:aman7303@localhost/solar_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'tif', 'tiff'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Database model
class SolarPotentialResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    image_path = db.Column(db.String(255), nullable=False)
    area = db.Column(db.Float, nullable=False)
    efficiency = db.Column(db.Float, nullable=False)
    avg_radiance = db.Column(db.Float, nullable=False)
    avg_radiance_model = db.Column(db.Float, nullable=False)
    solar_potential_api = db.Column(db.Float, nullable=False)
    solar_potential_model = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def fetch_solar_radiance(latitude, longitude, start_date, end_date):
    url = "https://power.larc.nasa.gov/api/temporal/daily/point"
    params = {
        'parameters': 'ALLSKY_SFC_SW_DWN',
        'community': 'RE',
        'longitude': longitude,
        'latitude': latitude,
        'start': start_date,
        'end': end_date,
        'format': 'json'
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        logger.error(f"Error fetching solar radiance: {response.status_code}")
        return None

def calculate_monthly_average_radiance(data):
    try:
        dates = []
        radiance_values = []
        for date, value in data['properties']['parameter']['ALLSKY_SFC_SW_DWN'].items():
            dates.append(datetime.datetime.strptime(date, '%Y%m%d'))
            radiance_values.append(value)
        df = pd.DataFrame({'date': dates, 'radiance': radiance_values})
        df.set_index('date', inplace=True)
        monthly_avg_radiance = df.resample('ME').mean()
        return monthly_avg_radiance
    except KeyError as e:
        logger.error(f"Error calculating monthly average radiance: {e}")
        return None

def calculate_solar_energy_potential(monthly_avg_radiance, area, efficiency):
    monthly_avg_radiance['total_energy'] = monthly_avg_radiance['radiance'] * area * efficiency * 365 / 12  # Energy in kWh/year
    return monthly_avg_radiance

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/calculate_solar_data', methods=['POST'])
def calculate_solar_data():
    data = request.json
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    coords = data.get('coordsArray')
    start_date = data.get('startDate', '20230101')
    end_date = data.get('endDate', '20231231')
    efficiency = data.get('efficiency', 0.18)

    if None in [latitude, longitude, coords]:
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        polygon = Polygon([(coord['lng'], coord['lat']) for coord in coords])
        polygon = orient(polygon, sign=1.0)
        area = polygon.area * (111139 * 111139)  # Approximate conversion to square meters

        solar_radiance_data = fetch_solar_radiance(latitude, longitude, start_date, end_date)
        
        if solar_radiance_data:
            monthly_avg_radiance = calculate_monthly_average_radiance(solar_radiance_data)
            if monthly_avg_radiance is not None:
                monthly_avg_radiance = calculate_solar_energy_potential(monthly_avg_radiance, area, efficiency)
                avg_radiance = monthly_avg_radiance['radiance'].mean()
                solar_potential_api = monthly_avg_radiance['total_energy'].sum()

                # Call calculate_solar_potential without image_path
                solar_potential_model = calculate_solar_potential(latitude, longitude, area=area)

                result = {
                    'area': area,
                    'avgRadiance': avg_radiance,
                    'solarPotentialAPI': solar_potential_api,
                    'solarPotentialModel': solar_potential_model['solar_potential'],
                    'modelAvgRadiance': solar_potential_model['avg_radiance'],
                    'totalBuildingArea': solar_potential_model['total_building_area'],
                    'imageArea': solar_potential_model['image_area']
                }

                return jsonify(result)

        return jsonify({'error': 'Could not calculate solar data from API'}), 500

    except Exception as e:
        logger.error(f"Error in calculate_solar_data: {str(e)}")
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500


@app.route('/api/save_image', methods=['POST'])
def save_image():
    data = request.json
    logger.info(f"Received data: {data}")

    latitude = data.get('latitude')
    longitude = data.get('longitude')
    coords = data.get('coordsArray')
    static_map_url = data.get('staticMapUrl')
    avg_radiance = data.get('avgRadiance', 0)
    model_avg_radiance = data.get('modelAvgRadiance', 0)
    solar_potential_api = data.get('solarPotentialAPI', 0)
    solar_potential_model = data.get('solarPotentialModel', 0)
    efficiency = data.get('efficiency', 0.18)

    if None in [latitude, longitude, coords, static_map_url]:
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        response = requests.get(static_map_url)
        filename = f'map_{latitude}_{longitude}.png'
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        os.makedirs(os.path.dirname(image_path), exist_ok=True)
        with open(image_path, 'wb') as f:
            f.write(response.content)
    except Exception as e:
        logger.error(f"Error saving image: {str(e)}")
        return jsonify({'error': 'Failed to save image'}), 500

    try:
        polygon = Polygon([(coord['lng'], coord['lat']) for coord in coords])
        polygon = orient(polygon, sign=1.0)
        area = polygon.area * (111139 * 111139)  # Approximate conversion to square meters
    except Exception as e:
        logger.error(f"Error calculating polygon area: {str(e)}")
        return jsonify({'error': 'Failed to calculate area'}), 500

    try:
        result = SolarPotentialResult(
            latitude=latitude,
            longitude=longitude,
            image_path=image_path,
            area=area,
            efficiency=efficiency,
            avg_radiance=avg_radiance,
            avg_radiance_model=model_avg_radiance,
            solar_potential_api=solar_potential_api,
            solar_potential_model=solar_potential_model
        )
        db.session.add(result)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error saving to database: {str(e)}")
        return jsonify({'error': 'Failed to save data to database'}), 500

    return jsonify({
        'imagePath': f'/static/images/{filename}',
        'area': area,
        'avgRadiance': avg_radiance,
        'modelAvgRadiance': model_avg_radiance,
        'solarPotentialAPI': solar_potential_api,
        'solarPotentialModel': solar_potential_model
    })

@app.route('/static/images/<path:filename>')
def serve_image(filename):
    return send_from_directory('static/images', filename)

@app.route('/api/results', methods=['GET'])
def get_results():
    results = SolarPotentialResult.query.all()
    return jsonify([{
        'id': result.id,
        'latitude': result.latitude,
        'longitude': result.longitude,
        'imagePath': result.image_path,
        'area': result.area,
        'efficiency': result.efficiency,
        'avgRadiance': result.avg_radiance,
        'avgRadianceModel': result.avg_radiance_model,
        'solarPotentialAPI': result.solar_potential_api,
        'solarPotentialModel': result.solar_potential_model,
        'timestamp': result.timestamp.isoformat()
    } for result in results])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)