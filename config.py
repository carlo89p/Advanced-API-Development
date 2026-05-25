import os
from dotenv import load_dotenv

load_dotenv()

class DevConfig:
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')