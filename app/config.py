import os
from datetime import timedelta

class Config:
    SECRET_KEY = 'ecovida_secret_key'
    JWT_SECRET_KEY = 'ecovida_jwt_secret_key'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    # Conexión a MySQL
    SQLALCHEMY_DATABASE_URI = os.getenv('MYSQL_URI', 'mysql+pymysql://root:ecovida@mysql:3306/ecovida')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Conexión a MongoDB
    MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://root:ecovida@mongodb:27017/ecovida?authSource=admin')
