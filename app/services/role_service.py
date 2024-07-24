from flask import Blueprint, request, jsonify
from extensions import db
from models.role import Role
from rabbitmq import enviar_mensaje_a_rabbitmq
import logging

bp = Blueprint('role_service', __name__)

@bp.route('/roles', methods=['GET'])
def obtener_roles():
    roles = Role.query.all()
    try:
        enviar_mensaje_a_rabbitmq('roles', 'Consulta de todos los roles realizada')
    except Exception as e:
        logging.error(f"Error al enviar mensaje a RabbitMQ: {e}")
    return jsonify([rol.as_dict() for rol in roles])

@bp.route('/roles/<int:id>', methods=['GET'])
def obtener_rol(id):
    rol = Role.query.get(id)
    try:
        enviar_mensaje_a_rabbitmq('roles', f'Consulta del rol con ID {id} realizada')
    except Exception as e:
        logging.error(f"Error al enviar mensaje a RabbitMQ: {e}")
    return jsonify(rol.as_dict()) if rol else ('', 404)

@bp.route('/roles', methods=['POST'])
def crear_rol():
    data = request.json

    max_id = db.session.query(db.func.max(Role.role_id)).scalar()
    nuevo_id = max_id + 1 if max_id is not None else 1

    nuevo_rol = Role(
        role_id=nuevo_id,
        role_name=data['role_name']
    )
    db.session.add(nuevo_rol)
    db.session.commit()
    try:
        enviar_mensaje_a_rabbitmq('roles', f'Rol creado: {nuevo_rol.as_dict()}')
    except Exception as e:
        print(f"Error al enviar mensaje a RabbitMQ: {e}")
    return jsonify(nuevo_rol.as_dict()), 201

@bp.route('/roles/<int:id>', methods=['PUT'])
def actualizar_rol(id):
    data = request.json
    rol = Role.query.get(id)
    if rol:
        for key, value in data.items():
            setattr(rol, key, value)
        db.session.commit()
        try:
            enviar_mensaje_a_rabbitmq('roles', f'Rol actualizado: {rol.as_dict()}')
        except Exception as e:
            logging.error(f"Error al enviar mensaje a RabbitMQ: {e}")
        return jsonify(rol.as_dict())
        return jsonify(rol.as_dict())
    else:
        return ('', 404)
    
@bp.route('/roles/<int:id>', methods=['DELETE'])
def eliminar_rol(id):
    rol = Role.query.get(id)
    if (rol):
        db.session.delete(rol)
        db.session.commit()
        try:
            enviar_mensaje_a_rabbitmq('roles', f'Rol eliminado: {rol.as_dict()}')
        except Exception as e:
            logging.error(f"Error al enviar mensaje a RabbitMQ: {e}")
        return ('', 204)
    else:
        return ('', 404)
    