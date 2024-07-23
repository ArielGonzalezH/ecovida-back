from run import create_app
from soap_services.inventario_service import init_app
from services.foundation_service import bp as foundation_service_bp
from services.product_service import bp as product_service_bp
from services.role_service import bp as role_service_bp
from services.sale_service import bp as sale_service_bp
from services.user_service import bp as user_service_bp

app = create_app()

# Configura los servicios SOAP
init_app(app)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=7000, debug=True)