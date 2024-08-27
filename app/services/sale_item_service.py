from flask import Blueprint, request, jsonify
from extensions import db
from models.sale_item import Sale_Item
from rabbitmq import enviar_mensaje_a_rabbitmq
import logging
from sqlalchemy import text

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

    max_id = db.session.query(db.func.max(Sale_Item.item_id)).scalar()
    nuevo_id = max_id + 1 if max_id is not None else 1

    nueva_venta = Sale_Item(
        item_id=nuevo_id,
        sale_header_id=data['sale_header_id'],
        product_id=data['product_id'],
        item_quantity=data['item_quantity']
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
    
@bp.route('/sale_items/<int:sale_header_id>', methods=['GET'])
def obtener_detalles_venta_por_encabezado(sale_header_id):
    """
    Consulta los detalles de los ítems de venta para un encabezado de venta específico.
    """
    try:
        # Consulta de ítems de venta para un solo SALE_HEADER_ID
        query = text("""
        SELECT
            si.ITEM_ID AS item_id,
            p.PRODUCT_NAME AS product_name,
            si.ITEM_QUANTITY AS item_quantity,
            p.PRODUCT_PRICE AS product_price
        FROM
            SALE_ITEMS si
        JOIN
            PRODUCT p
        ON
            si.PRODUCT_ID = p.PRODUCT_ID
        WHERE
            si.SALE_HEADER_ID = :sale_header_id;
        """)

        result = db.session.execute(query, {'sale_header_id': sale_header_id})
        
        # Convertir el resultado en una lista de diccionarios
        items = [dict(row._mapping) for row in result]
        
        return jsonify(items)
    except Exception as e:
        # Capturar el error específico
        error_message = str(e)
        print(f"Error al obtener los detalles de los ítems de venta: {error_message}")
        return jsonify({"error": "Error al obtener los detalles de los ítems de venta", "details": error_message}), 500