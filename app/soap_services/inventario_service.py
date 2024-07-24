from flask import Flask
from spyne import Application, rpc, ServiceBase, Integer, Unicode
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from extensions import db
from models import product
import logging

# Variable global para la aplicación Flask
flask_app = None

class InventarioService(ServiceBase):
    @rpc(Integer, _returns=Unicode)
    def consultar_inventario(ctx, product_id):
        logging.debug('Entering consultar_inventario method')
        # Usar el contexto de la aplicación global
        if flask_app:
            with flask_app.app_context():
                producto = product.Product.query.filter_by(product_id=product_id).first()
                if producto:
                    return f'Nombre: {producto.product_name}, Cantidad: {producto.product_stock}'
                else:
                    return 'Producto no encontrado'
        else:
            return 'Contexto de aplicación no disponible'

    @rpc(Integer, Integer, _returns=Unicode)
    def actualizar_inventario(ctx, product_id, cantidad):
        logging.debug('Entering actualizar_inventario method')
        # Usar el contexto de la aplicación global
        if flask_app:
            with flask_app.app_context():
                producto = product.Product.query.filter_by(product_id=product_id).first()
                if producto:
                    producto.product_stock = cantidad
                    db.session.commit()
                    return 'Actualización exitosa'
                else:
                    return 'Producto no encontrado'
        else:
            return 'Contexto de aplicación no disponible'

def init_app(app: Flask):
    global flask_app
    flask_app = app  # Guardar la referencia de la aplicación Flask

    soap_app = Application([InventarioService], 'spyne.examples.flask',
                           in_protocol=Soap11(validator='lxml'),
                           out_protocol=Soap11())
    wsgi_soap_app = WsgiApplication(soap_app)

    class SoapMiddleware:
        def __init__(self, app, wsgi_soap_app):
            self.app = app
            self.wsgi_soap_app = wsgi_soap_app

        def __call__(self, environ, start_response):
            path_info = environ.get('PATH_INFO', '')
            if isinstance(path_info, str) and path_info.startswith('/api/soap'):
                return self.wsgi_soap_app(environ, start_response)
            return self.app(environ, start_response)

    app.wsgi_app = SoapMiddleware(app.wsgi_app, wsgi_soap_app)
