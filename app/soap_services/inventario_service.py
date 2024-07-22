from spyne import Application, rpc, ServiceBase, Integer, Unicode
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication

class InventarioService(ServiceBase):
    @rpc(Integer, _returns=Unicode)
    def consultar_inventario(ctx, product_id):
        inventario = {
            1: {'nombre': 'Producto 1', 'cantidad': 50},
            2: {'nombre': 'Producto 2', 'cantidad': 20}
        }
        producto = inventario.get(product_id, None)
        return str(producto) if producto else 'Producto no encontrado'

    @rpc(Integer, Integer, _returns=Unicode)
    def actualizar_inventario(ctx, product_id, cantidad):
        inventario = {
            1: {'nombre': 'Producto 1', 'cantidad': 50},
            2: {'nombre': 'Producto 2', 'cantidad': 20}
        }
        if product_id in inventario:
            inventario[product_id]['cantidad'] = cantidad
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
                return self.wsgi_soap_app(environ, start_response)
            return self.app(environ, start_response)

    app.wsgi_app = SoapMiddleware(app.wsgi_app, wsgi_soap_app)