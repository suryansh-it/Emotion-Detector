
from sqlalchemy import create_engine, Table, Column, Integer, LargeBinary, MetaData, DateTime
from datetime import datetime

# Database Configuration
DATABASE_URL = 'postgresql://username:password@localhost/dbname'

# Create the engine and metadata
engine = create_engine(DATABASE_URL)
metadata = MetaData()

# Define the images table
images_table = Table(
    'images', metadata,
    Column('image_id', Integer, primary_key=True),
    Column('image', LargeBinary, nullable=False),
    Column('upload_time', DateTime, default=datetime.utcnow)
)

# Create the table if it doesn't exist
metadata.create_all(engine)
