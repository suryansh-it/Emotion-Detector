from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON
from datetime import datetime, timezone
import json
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
# Database Configuration





db = SQLAlchemy()

# Define the images table
class ImagesData(db.Model):
    __tablename__ = 'images_table'

    image_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    image_data = db.Column(db.Text,   nullable=False)
    upload_time = db.Column(db.DateTime,  default=lambda: datetime.now(timezone.utc))
    emotion_data = db.Column(db.String, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_table.id'), nullable=False)  # ForeignKey to the User model

    def to_dict(self):
        """Convert image model to dictionary, including binary data as base64."""
        return {
            'id': self.image_id,
            'upload_time': self.upload_time.isoformat(),
            'image_data': self.image_data,  # Base64 encoded image data
            'emotion_data': json.loads(self.emotion_data) if self.emotion_data else None
        }

 



class User(db.Model, UserMixin):
    __tablename__ = 'user_table'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    # Add a relationship to EmotionHistory
    emotions = db.relationship('EmotionHistory', backref='user', lazy=True)
    img_data = db.relationship('ImagesData', backref='images', lazy=True)


class EmotionHistory(db.Model):
    __tablename__ = 'history_table'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    emotions = db.Column(db.JSON, nullable=False)  # Store emotions as JSON
    dominant_emotion = db.Column(db.String, nullable=False)  # Store the dominant emotion
    user_id = db.Column(db.Integer, db.ForeignKey('user_table.id'), nullable=False)
