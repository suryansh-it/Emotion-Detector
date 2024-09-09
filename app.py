from flask import Flask, render_template, request, jsonify
from io import BytesIO
import os
import cv2
from fer import FER
from datetime import datetime
from sqlalchemy.sql import select
from models import engine, images_table

def create_app():
    app = Flask(__name__)

app = create_app()

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
def retrieve_image(image_id):
    with engine.connect() as connection:
        query = select([images_table.c.image]).where(images_table.c.image_id == image_id)
        result = connection.execute(query).fetchone()
        return result[0] if result else None

@app.route('/home', method= ['GET', 'POST'])
def capture():


@app.route('/home', method= ['GET', 'POST'])
def preview():


@app.route('/home' , method = ['GET'])
def emotion():


@app.route('home/login', method = ['GET' , 'POST'])
def login():

@app.route('home/Signup', method = ['GET' , 'POST'])
def signup():

@app.route('home/history' , method = ['GET'])
def history(): 

if __name__ == '__main__':
    app.run(debug=True)