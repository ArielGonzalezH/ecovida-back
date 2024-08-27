from flask import Blueprint, request, jsonify
from extensions import db
from models.sale_header import Sale_Header
from rabbitmq import enviar_mensaje_a_rabbitmq
import logging

bp = Blueprint('sale_header_service', __name__)

@bp.route('/sale_header', methods=['GET'])
def obtener_ventas():
    ventas = Sale_Header.query.all()
    try:
        enviar_mensaje_a_rabbitmq('sales', 'Consulta de todas las ventas realizada')
    except Exception as e:
        logging.error(f"Error al enviar mensaje a RabbitMQ: {e}")
    return jsonify([venta.as_dict() for venta in ventas])

@bp.route('/sale_header/<int:id>', methods=['GET'])
def obtener_venta(id):
    venta = Sale_Header.query.get(id)
    try:
        enviar_mensaje_a_rabbitmq('sales', f'Consulta de la venta con ID {id} realizada')
    except Exception as e:
        logging.error(f"Error al enviar mensaje a RabbitMQ: {e}")
    return jsonify(venta.as_dict()) if venta else ('', 404)


@bp.route('/sale_header', methods=['POST'])
def crear_venta():
    data = request.json

    max_id = db.session.query(db.func.max(Sale_Header.sh_id)).scalar()
    nuevo_id = max_id + 1 if max_id is not None else 1

    nueva_venta = Sale_Header(
        sh_id=nuevo_id,
        user_id=data['user_id'],
        sale_date=data['sale_date'],
        sale_sub=data['sale_sub'],
        sale_IVA=data['sale_IVA'],
        sale_total=data['sale_total']
    )
    db.session.add(nueva_venta)
    db.session.commit()
    try:
        print(f'Venta creada: {nueva_venta.as_dict()}')
        enviar_mensaje_a_rabbitmq('sales', f'Venta creada: {nueva_venta.as_dict()}')
    except Exception as e:
        print(f'Error al crear venta: {e}')
        logging.error(f"Error al enviar mensaje a RabbitMQ: {e}")
    return jsonify(nueva_venta.as_dict()), 201


@bp.route('/sale_header/<int:id>', methods=['PUT'])
def actualizar_venta(id):
    data = request.json
    venta = Sale_Header.query.get(id)
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
    
    
@bp.route('/sale_header/<int:id>', methods=['DELETE'])
def eliminar_venta(id):
    venta = Sale_Header.query.get(id)
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
    
@bp.route('/sale_header/<int:user_id>', methods=['GET'])
def getLatestSaleHeader(user_id):
    venta = Sale_Header.query.filter(Sale_Header.user_id == user_id) \
                              .order_by(Sale_Header.sale_date.desc()) \
                              .first()
    try:
        enviar_mensaje_a_rabbitmq('sales', f'Consulta de la venta más reciente para el usuario con ID {user_id} realizada')
    except Exception as e:
        logging.error(f"Error al enviar mensaje a RabbitMQ: {e}")
    
    return jsonify(venta.as_dict()) if venta else ('', 404)