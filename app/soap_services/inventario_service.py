# soap_service.py
from flask import Flask
from spyne import Application, rpc, ServiceBase, Integer, Unicode
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from extensions import db
from models import product

class InventarioService(ServiceBase):
    @rpc(Integer, _returns=Unicode)
    def consultar_inventario(ctx, product_id):
        with ctx.udc.app.app_context():
            producto = product.Product.query.filter_by(product_id=product_id).first()
            if producto:
                return f'Nombre: {producto.product_name}, Cantidad: {producto.product_stock}'
            else:
                return 'Producto no encontrado'

    @rpc(Integer, Integer, _returns=Unicode)
    def actualizar_inventario(ctx, product_id, cantidad):
        with ctx.udc.app.app_context():
            producto = product.Product.query.filter_by(product_id=product_id).first()
            if producto:
                producto.product_stock = cantidad
                db.session.commit()
                return 'Actualización exitosa'
            else:
                return 'Producto no encontrado'

def init_app(app):
    soap_app = Application([InventarioService], 'spyne.examples.flask',
                           in_protocol=Soap11(validator='lxml'),
                           out_protocol=Soap11())
    wsgi_soap_app = WsgiApplication(soap_app)

    class SoapMiddleware:
        def __init__(self, app, wsgi_soap_app):
            self.app = app
            self.wsgi_soap_app = wsgi_soap_app

        def __call__(self, environ, start_response):
            if environ['PATH_INFO'].startswith('/api/soap'):
                environ['spyne.udc'] = {'app': self.app}
                return self.wsgi_soap_app(environ, start_response)
            return self.app(environ, start_response)

    app.wsgi_app = SoapMiddleware(app.wsgi_app, wsgi_soap_app)
