from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.user import User

bp = Blueprint('user_service', __name__)

@bp.route('/usuarios', methods=['GET'])
def obtener_usuarios():
    usuarios = User.query.all()
    return jsonify([usuario.as_dict() for usuario in usuarios])

@bp.route('/usuarios/<int:id>', methods=['GET'])
def obtener_usuario(id):
    usuario = User.query.get(id)
    return jsonify(usuario.as_dict()) if usuario else ('', 404)

@bp.route('/usuarios', methods=['POST'])
def crear_usuario():
    data = request.json
    nuevo_usuario = User(**data)
    db.session.add(nuevo_usuario)
    db.session.commit()
    return jsonify(nuevo_usuario.as_dict()), 201

@bp.route('/usuarios/<int:id>', methods=['PUT'])
def actualizar_usuario(id):
    data = request.json
    usuario = User.query.get(id)
    if usuario:
        for key, value in data.items():
            setattr(usuario, key, value)
        db.session.commit()
        return jsonify(usuario.as_dict())
    else:
        return ('', 404)
    
@bp.route('/usuarios/<int:id>', methods=['DELETE'])
def eliminar_usuario(id):
    usuario = User.query.get(id)
    if (usuario):
        db.session.delete(usuario)
        db.session.commit()
        return ('', 204)
    else:
        return ('', 404)
    
@bp.route('/usuarios/login', methods=['POST'])
def login():
    data = request.json
    usuario = User.query.filter_by(email=data['email']).first()
    if usuario and usuario.check_password(data['password']):
        return jsonify(usuario.as_dict())
    else:
        return ('', 401)
    
@bp.route('/usuarios/registro', methods=['POST'])
def registro():
    data = request.json
    nuevo_usuario = User(**data)
    db.session.add(nuevo_usuario)
    db.session.commit()
    return jsonify(nuevo_usuario.as_dict()), 201