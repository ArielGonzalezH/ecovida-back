import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('MYSQL_URI', 'mysql://root:aagonzalez8@mysql/ecovida')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')
    MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://mongo:27017/ecovida')
