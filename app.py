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
def retrieve_image(image_ids):
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
@app.route('/home', method= ['GET', 'POST'])
def capture():
    file = request.files['file']
    image_bytes = file.read()   #read img as bytes


    #store img 
    image_id = store_image(image_bytes)
    return jsonify({'image_id': image_id})


# Route 2: Preview 3 Captured Images
@app.route('/home', method= ['GET', 'POST'])
def preview():
# Query to get the last 3 images stored in the database



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