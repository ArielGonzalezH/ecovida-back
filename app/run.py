import pymysql
pymysql.install_as_MySQLdb()

from flask import Flask
from flask_jwt_extended import JWTManager
from config import Config
from extensions import db, bcrypt
from flask_pymongo import PyMongo
from flask_cors import CORS  # Importa CORS
from services import foundation_service, product_service, role_service, sale_service, user_service
from soap_services import inventario_service

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Configura CORS
    CORS(app, resources={r"/*": {"origins": "*"}}) 

    db.init_app(app)
    bcrypt.init_app(app)
    
    # Configuración de MongoDB
    mongo = PyMongo(app, uri=app.config['MONGODB_URI'])

    jwt = JWTManager(app)

    # Inicializar servicios SOAP
    inventario_service.init_app(app)

    # Registrar Blueprints REST
    app.register_blueprint(foundation_service.bp, url_prefix='/api/foundations')
    app.register_blueprint(product_service.bp, url_prefix='/api/products')
    app.register_blueprint(role_service.bp, url_prefix='/api/roles')
    app.register_blueprint(sale_service.bp, url_prefix='/api/sales')
    app.register_blueprint(user_service.bp, url_prefix='/api/users')

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0', port=7000, debug=True)
