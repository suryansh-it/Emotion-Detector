from flask import Flask, render_template, request, jsonify, flash, url_for, redirect
import json
from io import BytesIO
import os
import cv2
import numpy as np
from fer import FER
from sqlalchemy.sql import select
from models import db , ImagesData,User , EmotionHistory
from flask_migrate import Migrate
import base64
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from form import Signupform, LoginForm
from capture_image import *

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI']  = 'postgresql://postgres:0904@localhost:5432/emotion_det'
    db.init_app(app)

    with app.app_context():
        db.create_all()
    
    return app


app = create_app()
migrate = Migrate(app,db)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
bcrypt = Bcrypt(app)

# Initialize FER emotion detector
emotion_detector = FER()

@app.route('/')
def home() :
    return render_template('index.html')



# Function to detect emotion using FER and OpenCV
def detect_emotion(image_data):
    # Convert the image bytes to a NumPy array
    image = cv2.imdecode(np.frombuffer(base64.b64decode(image_data), np.uint8), cv2.IMREAD_COLOR)
    
    # Detect emotions on the image using FER
    emotion_results = emotion_detector.detect_emotions(image)

    if not emotion_results:
        return {"error": "No face detected."}

    # Get the emotion with the highest confidence score
    emotions = emotion_results[0]['emotions']
    
    return emotions


# # Store image temporarily in PostgreSQL
# def store_image(image_data):
#     if request.method == 'POST':
#         data =request.get_json


#     with engine.connect() as connection:
#         insert_query = images_table.insert().values(image=image_bytes, upload_time=datetime.now())
#         result = connection.execute(insert_query)
#         return result.inserted_primary_key[0]
    

# # Retrieve image by image_id
# def retrieve_images(image_ids):
#     with engine.connect() as connection:
#         query = select([images_table.c.image, images_table.c.image_id]).where(images_table.c.image_id.in_(image_ids))
#         result = connection.execute(query).fetchall()
#         return [{'image_id': row['image_id'], 'image': row['image']} for row in result]
    

# delete imag after use
def delete_image ():
    images = ImagesData.query.order_by(ImagesData.upload_time.desc()).limit(3).all()
    db.session.delete(images)
    db.session.commit()
    return jsonify({'message': 'project post deleted'})
#     with engine.connect() as connection:
#         delete_query = images_table.delete().where(images_table.c.image_id == image_id)
#         connection.execute(delete_query)



# User loader function
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



# Route 1: Capture Images

@app.route('/capture', methods=['POST'])
def capture():
    try:
        # Get image data from the request
        image_data = request.json['image_data']

        # Check if the current user is logged in
        if not current_user.is_authenticated:
            return jsonify({'error': 'User not authenticated'}), 401

        # Save the captured image in the database
        new_image = ImagesData(image_data=image_data, user_id=current_user.id)  # Directly store the Base64 string
        db.session.add(new_image)
        db.session.commit()

        # Return success response
        return jsonify({'message': 'Image captured successfully', 'image_id': new_image.image_id}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Route 2: Preview 3 Captured Images


@app.route('/preview', methods=['GET'])
@login_required
def preview():
    try:
        # Get the last 3 images for the currently logged-in user
        images = ImagesData.query.filter_by(user_id=current_user.id)\
            .order_by(ImagesData.upload_time.desc()).limit(3).all()


        # Fetch all images for the user, excluding the last 3 images
        all_images = ImagesData.query.filter_by(user_id=current_user.id).all()
        images_to_delete = [image for image in all_images if image not in images]


        images_json = []
        for image in images:
            if image.image_data:
                # No need to convert image_data to bytes; it's already in Base64 format
                images_json.append({
                    "id": image.image_id,  # Include image ID
                    "image_data": image.image_data})  # Store the Base64 string directly
            else:
                return jsonify({'error': 'Image data is missing for one or more images.'}), 500


        # Delete older images (those not in the last 3)
        for image in images_to_delete:
            db.session.delete(image)
        
        # Commit the deletion changes
        db.session.commit()


        return jsonify(images_json), 200

    except Exception as e:
        print(f"Error in preview route: {e}")
        return jsonify({'error': f'An internal error occurred: {str(e)}'}), 500



# Route 3: Select One Image for Emotion Detection
@app.route('/detectemotion/<int:image_id>', methods=['GET'])
@login_required
def detectemotion(image_id):
    try:
        image = ImagesData.query.get(image_id)

        if not image:
            return jsonify({'error': 'Image not found'}), 404

        # Assuming detect_emotion is a function that takes a base64-encoded image and returns emotion data
        emotions = detect_emotion(image.image_data)  # image.image_data is already base64 encoded

        # Store the detected emotions in the image record (as JSON)
        image.emotion_data = json.dumps(emotions)
        db.session.commit()

        # Save the emotion history in a separate table
        new_record = EmotionHistory(
            emotions=json.dumps(emotions),
            user_id=current_user.id
        )
        db.session.add(new_record)
        db.session.commit()

        # Optionally, delete the image after detection if required
        # delete_image(image_id)

        return jsonify(emotions), 200

    except Exception as e:
        return jsonify({'error': f'An internal error occurred: {str(e)}'}), 500


@app.route('/home/login', methods = ['GET' , 'POST'])
def login():
    form= LoginForm()
    if form.validate_on_submit():
        user= User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        
        else:
            flash('Login failed. Check your email and/or password', 'danger')
    return render_template('login.html', title='Login', form=form)




@app.route('/home/signup', methods = ['GET' , 'POST'])
def signup():
    form = Signupform()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data, email= form.email.data, password= hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', title='Sign Up', form=form)




@app.route('/home/history' , methods = ['GET'])
@login_required
def history():

    try: 
        # Query to get emotion history for the current user
        emotion_history = EmotionHistory.query.filter_by(user_id =current_user.id).order_by(EmotionHistory.detected_at.desc()).all()
        return render_template('history.html', emotion_history=emotion_history)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/home/logout')
def logout():
    logout_user()  # This will log out the user
    flash('You have been logged out!', 'info')  # Optionally flash a message
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)