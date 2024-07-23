from flask import Blueprint, request, jsonify
from extensions import db
from models.role import Role

bp = Blueprint('role_service', __name__)

@bp.route('/roles', methods=['GET'])
def obtener_roles():
    roles = Role.query.all()
    return jsonify([rol.as_dict() for rol in roles])

@bp.route('/roles/<int:id>', methods=['GET'])
def obtener_rol(id):
    rol = Role.query.get(id)
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
    return jsonify(nuevo_rol.as_dict()), 201

@bp.route('/roles/<int:id>', methods=['PUT'])
def actualizar_rol(id):
    data = request.json
    rol = Role.query.get(id)
    if rol:
        for key, value in data.items():
            setattr(rol, key, value)
        db.session.commit()
        return jsonify(rol.as_dict())
    else:
        return ('', 404)
    
@bp.route('/roles/<int:id>', methods=['DELETE'])
def eliminar_rol(id):
    rol = Role.query.get(id)
    if (rol):
        db.session.delete(rol)
        db.session.commit()
        return ('', 204)
    else:
        return ('', 404)
    