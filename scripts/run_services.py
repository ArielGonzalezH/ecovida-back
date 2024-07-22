from app import create_app
from app.soap_services.inventario_service import init_app
from app.services.foundation_service import bp as foundation_service_bp
from app.services.product_service import bp as product_service_bp
from app.services.role_service import bp as role_service_bp
from app.services.sale_service import bp as sale_service_bp
from app.services.user_service import bp as user_service_bp

app = create_app()

# Configura los servicios SOAP
init_app(app)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)