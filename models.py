from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash

# Database Configuration
DATABASE_URL = 'postgresql://postgres:0904@localhost:5432/'




db = SQLAlchemy()

# Define the images table
class Images(db.Model):
    __tablename__ = 'images_table'

    image_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    image = db.Column(db.LargeBinary,   nullable=False)
    upload_time = db.Column(db.DateTime,  default=lambda: datetime.now(timezone.utc))
 
