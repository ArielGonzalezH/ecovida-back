from flask import Blueprint, request, jsonify
from extensions import db
from models.package import Package
from datetime import datetime
from rabbitmq import enviar_mensaje_a_rabbitmq
import logging

bp = Blueprint('package_service', __name__)

@bp.route('/package', methods=['GET'])
def obtener_paquetes():
    paquetes = Package.query.all()
    try:
        enviar_mensaje_a_rabbitmq('package', 'Consulta de todos los paquetes realizada')
    except Exception as e:
        logging.error(f"Error al enviar mensaje a RabbitMQ: {e}")
    return jsonify([paquete.as_dict() for paquete in paquetes])

@bp.route('/package/<int:id>', methods=['GET'])
def obtener_paquete(id):
    paquete = Package.query.get(id)
    try:
        enviar_mensaje_a_rabbitmq('package', f'Consulta del paquete con ID {id} realizada')
    except Exception as e:
        logging.error(f"Error al enviar mensaje a RabbitMQ: {e}")
    return jsonify(paquete.as_dict()) if paquete else ('', 404)

@bp.route('/package', methods=['POST'])
def crear_paquete():
    max_id = db.session.query(db.func.max(Package.package_id)).scalar()
    nuevo_id = max_id + 1 if max_id is not None else 1  
    data = request.json

    # Establecer siempre el estado inicial como "Verificado"
    nuevo_paquete = Package(
        package_id=nuevo_id,
        sale_header_id=data['sale_header_id'],
        state_package="Verificado",  # Estado inicial siempre "Verificado"
        date_verification=datetime.utcnow()  # Fecha de verificación establecida al crear el paquete
    )
    db.session.add(nuevo_paquete)
    db.session.commit()
    try:
        enviar_mensaje_a_rabbitmq('package', f'Paquete creado: {nuevo_paquete.as_dict()}')
    except Exception as e:
        logging.error(f"Error al enviar mensaje a RabbitMQ: {e}")
    return jsonify(nuevo_paquete.as_dict()), 201

@bp.route('/package/<int:id>', methods=['PUT'])
def actualizar_paquete(id):
    data = request.json
    paquete = Package.query.get(id)
    if paquete:
        state_changed = False
        if 'state_package' in data:
            new_state = data['state_package']
            if new_state != paquete.state_package:
                state_changed = True
                paquete.state_package = new_state
                # Actualizar las fechas según el nuevo estado
                if new_state == "Enviado":
                    paquete.date_shipping = datetime.utcnow()  # Guardar la fecha y hora actual
                elif new_state == "Entregado":
                    paquete.date_delivery = datetime.utcnow()  # Guardar la fecha y hora actual
        
        for key, value in data.items():
            if key != 'state_package':  # Ya lo manejamos arriba
                setattr(paquete, key, value)

        db.session.commit()
        try:
            enviar_mensaje_a_rabbitmq('package', f'Paquete actualizado: {paquete.as_dict()}')
        except Exception as e:
            logging.error(f"Error al enviar mensaje a RabbitMQ: {e}")
        return jsonify(paquete.as_dict())
    else:
        return ('', 404)

@bp.route('/package/<int:id>', methods=['DELETE'])
def eliminar_paquete(id):
    paquete = Package.query.get(id)
    if paquete:
        db.session.delete(paquete)
        db.session.commit()
        try:
            enviar_mensaje_a_rabbitmq('package', f'Paquete eliminado: {paquete.as_dict()}')
        except Exception as e:
            logging.error(f"Error al enviar mensaje a RabbitMQ: {e}")
        return ('', 204)
    else:
        return ('', 404)
