from flask import Flask
from flask_jwt_extended import JWTManager
from config import Config
from extensions import db, bcrypt, mongo  # Asegúrate de importar mongo
from flask_cors import CORS
from services import (foundation_service, product_service, role_service,
                      sale_service, user_service, sale_header_service, sale_item_service)
from soap_services import inventario_service
from services.comment_service import bp as comment_service_bp  # Importar el blueprint de comentarios

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Configura CORS
    CORS(app, resources={r"/*": {"origins": "*"}})

    db.init_app(app)
    bcrypt.init_app(app)
    
    # Configuración de MongoDB
    mongo.init_app(app)  # Asegúrate de que esto esté en `create_app`

    jwt = JWTManager(app)

    # Inicializar servicios SOAP
    inventario_service.init_app(app)

    # Registrar Blueprints REST
    app.register_blueprint(foundation_service.bp, url_prefix='/api/foundations')
    app.register_blueprint(product_service.bp, url_prefix='/api/products')
    app.register_blueprint(role_service.bp, url_prefix='/api/roles')
    app.register_blueprint(sale_service.bp, url_prefix='/api/sales')
    app.register_blueprint(user_service.bp, url_prefix='/api/users')
    app.register_blueprint(sale_header_service.bp, url_prefix='/api/sale_headers')
    app.register_blueprint(sale_item_service.bp, url_prefix='/api/sale_items')
    app.register_blueprint(comment_service_bp, url_prefix='/api/comments')  # Registrar el blueprint de comentarios

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0', port=7000, debug=True)