from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON
from datetime import datetime, timezone
import json
from werkzeug.security import generate_password_hash, check_password_hash

# Database Configuration





db = SQLAlchemy()

# Define the images table
class ImagesData(db.Model):
    __tablename__ = 'images_table'

    image_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    image = db.Column(db.LargeBinary,   nullable=False)
    upload_time = db.Column(db.DateTime,  default=lambda: datetime.now(timezone.utc))
    emotion_data = db.Column(db.String, nullable=True)

    def to_dict(self):
        """Convert image model to dictionary, omitting binary data."""
        return {
            'id': self.id,
            'upload_time': self.upload_time.isoformat(),
            'emotion_data': json.loads(self.emotion_data) if self.emotion_data else None
        }
 
