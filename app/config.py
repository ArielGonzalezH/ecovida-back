import os

class Config:
    SECRET_KEY = 'ecovida_secret'
    # Conexión a MySQL
    SQLALCHEMY_DATABASE_URI = os.getenv('MYSQL_URI', 'mysql+pymysql://root:ecovida@mysql:3306/ecovida')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Clave secreta para la aplicación
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')
    
    # Conexión a MongoDB
    MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://root:ecovida@mongodb:27017/ecovida?authSource=admin')
