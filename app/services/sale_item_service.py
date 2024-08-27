from flask import Blueprint, request, jsonify
from extensions import db
from models.sale_item import Sale_Item
from rabbitmq import enviar_mensaje_a_rabbitmq
import logging

bp = Blueprint('sale_item_service', __name__)

@bp.route('/sale_item', methods=['GET'])
def obtener_ventas():
    ventas = Sale_Item.query.all()
    try:
        enviar_mensaje_a_rabbitmq('sales', 'Consulta de todas las ventas realizada')
    except Exception as e:
        logging.error(f"Error al enviar mensaje a RabbitMQ: {e}")
    return jsonify([venta.as_dict() for venta in ventas])

@bp.route('/sale_item/<int:id>', methods=['GET'])
def obtener_venta(id):
    venta = Sale_Item.query.get(id)
    try:
        enviar_mensaje_a_rabbitmq('sales', f'Consulta de la venta con ID {id} realizada')
    except Exception as e:
        logging.error(f"Error al enviar mensaje a RabbitMQ: {e}")
    return jsonify(venta.as_dict()) if venta else ('', 404)


@bp.route('/sale_item', methods=['POST'])
def crear_venta():
    data = request.json

    max_id = db.session.query(db.func.max(Sale_Item.sale_id)).scalar()
    nuevo_id = max_id + 1 if max_id is not None else 1

    nueva_venta = Sale_Item(
        item_id=nuevo_id,
        sale_header_id=data['sale_header_id'],
        product_id=data['product_id'],
        sale_quantity=data['sale_quantity']
    )
    db.session.add(nueva_venta)
    db.session.commit()
    try:
        enviar_mensaje_a_rabbitmq('sales', f'Item creado: {nueva_venta.as_dict()}')
    except Exception as e:
        logging.error(f"Error al enviar mensaje a RabbitMQ: {e}")
    return jsonify(nueva_venta.as_dict()), 201


@bp.route('/sale_item/<int:id>', methods=['PUT'])
def actualizar_venta(id):
    data = request.json
    venta = Sale_Item.query.get(id)
    if venta:
        for key, value in data.items():
            setattr(venta, key, value)
        db.session.commit()
        try:
            enviar_mensaje_a_rabbitmq('sales', f'Venta actualizada: {venta.as_dict()}')
        except Exception as e:
            logging.error(f"Error al enviar mensaje a RabbitMQ: {e}")
        return jsonify(venta.as_dict())
    else:
        return ('', 404)
    
    
@bp.route('/sale_item/<int:id>', methods=['DELETE'])
def eliminar_venta(id):
    venta = Sale_Item.query.get(id)
    if (venta):
        db.session.delete(venta)
        db.session.commit()
        try:
            enviar_mensaje_a_rabbitmq('sales', f'Venta eliminada: {venta.as_dict()}')
        except Exception as e:
            logging.error(f"Error al enviar mensaje a RabbitMQ: {e}")
        return ('', 204)
    else:
        return ('', 404)