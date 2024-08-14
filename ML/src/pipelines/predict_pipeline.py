# import numpy as np
# from roboflow import Roboflow
# import cv2
# from flask import current_app
# import requests
# from io import BytesIO
# import tempfile

# def predict_pipeline(db, Polygon):
#     rf = Roboflow(api_key="S0Ge3PviIu86zB3iTNei")
#     project = rf.workspace().project("buidling-footprint")
#     model = project.version(1).model

#     # Query the latest Polygon entry from the database
#     with current_app.app_context():
#         latest_polygon = db.session.query(Polygon).order_by(Polygon.created_at.desc()).first()

#     if not latest_polygon:
#         print("No polygon found in the database.")
#         return

#     image_url = latest_polygon.image_url

#     # Download the image
#     response = requests.get(image_url)
#     image = cv2.imdecode(np.frombuffer(response.content, np.uint8), -1)

#     # Save the image to a temporary file
#     with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as temp_file:
#         cv2.imwrite(temp_file.name, image)
#         temp_file_path = temp_file.name

#     # Make prediction using the temporary file path
#     prediction = model.predict(temp_file_path).json()

#     image_height, image_width = image.shape[:2]

#     for obj in prediction['predictions']:
#         points = obj['points']
        
#         mask = np.zeros((image_height, image_width), dtype=np.uint8)
        
#         polygon = np.array([[int(point['x']), int(point['y'])] for point in points], dtype=np.int32)
#         cv2.fillPoly(mask, [polygon], 255)  
        
#         area = np.sum(mask > 0)
        
#         class_name = obj['class']
#         confidence = obj['confidence']
        
#         print(f"Class: {class_name}, Confidence: {confidence:.2f}, Area: {area} pixels")

#     # Save the annotated prediction
#     model.predict(temp_file_path).save("annotated_prediction.jpg")

#     print("Prediction completed and saved as annotated_prediction.jpg")

#     # Clean up the temporary file
#     import os
#     os.unlink(temp_file_path)

# def run_prediction(db, Polygon):
#     predict_pipeline(db, Polygon)

# if __name__ == "__main__":
#     from flask import Flask
#     from flask_sqlalchemy import SQLAlchemy
    
#     app = Flask(__name__)
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://aman:aman7303@localhost/solar_db'
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#     db = SQLAlchemy(app)
    
#     class Polygon(db.Model):
#         id = db.Column(db.Integer, primary_key=True)
#         user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#         coordinates = db.Column(db.Text, nullable=False)
#         image_path = db.Column(db.String(255))
#         created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
#         image_url = db.Column(db.String(255))

#     with app.app_context():
#         run_prediction(db, Polygon)
import numpy as np
import cv2
import torch
from flask import current_app
import requests
from io import BytesIO
import tempfile
import os

def predict_pipeline(db, Polygon):
    # Load YOLOv8 model
    model_path = r'D:\Rooftop-Solar-Energy-Potential-Map\ML\models\best.pt'
    from ultralytics import YOLO
    model = YOLO(model_path)
    
    # Query the latest Polygon entry from the database
    with current_app.app_context():
        latest_polygon = db.session.query(Polygon).order_by(Polygon.created_at.desc()).first()

    if not latest_polygon:
        print("No polygon found in the database.")
        return

    image_url = latest_polygon.image_url

    # Download the image
    response = requests.get(image_url)
    image = cv2.imdecode(np.frombuffer(response.content, np.uint8), -1)

    # Save the image to a temporary file
    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as temp_file:
        cv2.imwrite(temp_file.name, image)
        temp_file_path = temp_file.name

    # Make prediction using the temporary file path
    results = model.predict(temp_file_path)  # This returns a Results object
    
    # Process predictions
    for result in results:  # Iterate over the Results object
        if len(result.boxes) == 0:  # Check if there are no detections
            continue
        
        image_height, image_width = image.shape[:2]
        
        for box in result.boxes:  # Iterate over detected boxes
            x1, y1, x2, y2 = box.xyxy[0].tolist()  # Extract bounding box coordinates
            class_id = int(box.cls)  # Extract class ID
            conf = box.conf[0]  # Extract confidence
            
            # Create mask for the detected object
            mask = np.zeros((image_height, image_width), dtype=np.uint8)
            polygon = np.array([[x1, y1], [x2, y1], [x2, y2], [x1, y2]], dtype=np.int32)  # Simplified bounding box to polygon
            cv2.fillPoly(mask, [polygon], 255)
            
            # Calculate the area of the mask
            area = np.sum(mask > 0)
            
            class_name = model.names[class_id]  # Get class name
            print(f"Class: {class_name}, Confidence: {conf:.2f}, Area: {area} pixels")
            

    # Clean up the temporary file
    os.unlink(temp_file_path)

def run_prediction(db, Polygon):
    predict_pipeline(db, Polygon)
    # annotated_image_path='D:\Rooftop-Solar-Energy-Potential-Map\ML\src\pipelines\annotated_prediction.jpg'

if __name__ == "__main__":
    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy
    
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://aman:aman7303@localhost/solar_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db = SQLAlchemy(app)
    
    class Polygon(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
        coordinates = db.Column(db.Text, nullable=False)
        image_path = db.Column(db.String(255))
        created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
        image_url = db.Column(db.String(255))

    with app.app_context():
        run_prediction(db, Polygon)











