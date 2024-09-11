from flask import Flask, render_template, request, jsonify
from io import BytesIO
import os
import cv2
import numpy as np
from fer import FER
from datetime import datetime
from sqlalchemy.sql import select
from models import db , Images
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from wtforms import StringField , PasswordField , SubmitField
from wtforms.validators import InputRequired , Length, ValidationError

def create_app():
    app = Flask(__name__)

    db.init_app(app)

    with app.app_context():
        db.create_all()
    
    return app


app = create_app()
migrate = Migrate(app,db)

# Initialize FER emotion detector
emotion_detector = FER()

@app.route('/')
def home() :
    render_template('index.html')



# Function to detect emotion using FER and OpenCV
def detect_emotion(image_bytes):
    # Convert the image bytes to a NumPy array
    image = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
    
    # Detect emotions on the image using FER
    emotion_results = emotion_detector.detect_emotions(image)

    if not emotion_results:
        return {"error": "No face detected."}

    # Get the emotion with the highest confidence score
    emotions = emotion_results[0]['emotions']
    
    return emotions


# Store image temporarily in PostgreSQL
def store_image(image_bytes):
    with engine.connect() as connection:
        insert_query = images_table.insert().values(image=image_bytes, upload_time=datetime.now())
        result = connection.execute(insert_query)
        return result.inserted_primary_key[0]
    

# Retrieve image by image_id
def retrieve_images(image_ids):
    with engine.connect() as connection:
        query = select([images_table.c.image, images_table.c.image_id]).where(images_table.c.image_id.in_(image_ids))
        result = connection.execute(query).fetchall()
        return [{'image_id': row['image_id'], 'image': row['image']} for row in result]
    

#delete imag after use
def delete_image (image_id):
    with engine.connect() as connection:
        delete_query = images_table.delete().where(images_table.c.image_id == image_id)
        connection.execute(delete_query)




# Route 1: Capture Images
@app.route('/home/capture', method= ['GET', 'POST'])
def capture():
    file = request.files['file']
    image_bytes = file.read()   #read img as bytes


    #store img 
    image_id = store_image(image_bytes)
    return jsonify({'image_id': image_id})


# Route 2: Preview 3 Captured Images
@app.route('/home/preview_images', method= ['GET', 'POST'])
def preview():
# Query to get the last 3 images stored in the database
    with engine.connect() as connection:
        query = select([images_table.c.image_id]).order_by(images_table.c.upload_time.desc()).limit(3)
        result = connection.execute(query).fetchall()
        image_ids = [row['image_id'] for row in result]


     # Retrieve the 3 images using their IDs
    images = retrieve_images(image_ids)

     # Convert the image data to something the frontend can display (e.g., Base64)
    preview_images = [{'image_id': img['image_id'], 'image': img['image']} for img in images]

    return jsonify(preview_images)


# Route 3: Select One Image for Emotion Detection
@app.route('home/detect_emotion/<int:image_id>', methods=['GET'])
def detectemotion(image_id):
    # Retrieve the image from PostgreSQL
    with engine.connect() as connection:
        query =select([images_table.c.image]).where(images_table.c.image_id == image_id)
        result = connection.execute(query).fetchone

        if not result :
            return jsonify({'error': 'image not found'}), 404
        
    image_bytes= result['image']

    # Detect emotion using the retrieved image
    emotions = detect_emotion(image_bytes)

    # Delete the image after emotion detection
    delete_image(image_id)

    return jsonify(emotions)


@app.route('home/login', method = ['GET' , 'POST'])
def login():


@app.route('home/Signup', method = ['GET' , 'POST'])
def signup():

@app.route('home/history' , method = ['GET'])
def history(): 

if __name__ == '__main__':
    app.run(debug=True)