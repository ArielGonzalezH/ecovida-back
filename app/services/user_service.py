from flask import Blueprint, request, jsonify
from extensions import db
from models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, decode_token

bp = Blueprint('user_service', __name__)

@bp.route('/usuarios', methods=['GET'])
@jwt_required()
def obtener_usuarios():
    usuarios = User.query.all()
    return jsonify([usuario.as_dict() for usuario in usuarios])

@bp.route('/usuarios/<int:id>', methods=['GET'])
@jwt_required()
def obtener_usuario(id):
    usuario = User.query.get(id)
    return jsonify(usuario.as_dict()) if usuario else ('', 404)

@bp.route('/usuarios', methods=['POST'])
def crear_usuario():
    data = request.json

    # Obtener el ID máximo actual en la base de datos
    max_id = db.session.query(db.func.max(User.user_id)).scalar()
    nuevo_id = max_id + 1 if max_id is not None else 1

    nuevo_usuario = User(
        user_id=nuevo_id,
        role_id=data['role_id'],
        user_name=data['user_name'],
        user_lastname=data['user_lastname'],
        user_email=data['user_email'],
        user_password=generate_password_hash(data['user_password'])
    )
    
    db.session.add(nuevo_usuario)
    db.session.commit()
    
    auth_token = create_access_token(identity={
        'user': nuevo_usuario.user_id,
        'type': nuevo_usuario.role_id,
        'name': nuevo_usuario.user_name,
        'email': nuevo_usuario.user_email
    })
    
    return jsonify({'token': auth_token, 'usuario': nuevo_usuario.as_dict()}), 201

@bp.route('/usuarios/<int:id>', methods=['PUT'])
@jwt_required()
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
@jwt_required()
def eliminar_usuario(id):
    usuario = User.query.get(id)
    if usuario:
        db.session.delete(usuario)
        db.session.commit()
        return ('', 204)
    else:
        return ('', 404)

@bp.route('/usuarios/login', methods=['POST'])
def login():
    data = request.json
    usuario = User.query.filter_by(user_email=data['user_email']).first()
    if usuario and check_password_hash(usuario.user_password, data['user_password']):
        auth_token = create_access_token(identity={
            'user': usuario.user_id,
            'type': usuario.role_id,
            'name': usuario.user_name,
            'email': usuario.user_email
        })
        return jsonify({'token': auth_token, 'usuario': usuario.as_dict()})
    else:
        return ('', 401)

@bp.route('/usuarios/registro', methods=['POST'])
def registro():
    data = request.json

    max_id = db.session.query(db.func.max(User.user_id)).scalar()
    nuevo_id = max_id + 1 if max_id is not None else 1

    nuevo_usuario = User(
        user_id=nuevo_id,
        role_id=data['role_id'],
        user_name=data['user_name'],
        user_lastname=data['user_lastname'],
        user_email=data['user_email'],
        user_password=generate_password_hash(data['user_password'])
    )
    db.session.add(nuevo_usuario)
    db.session.commit()
    
    auth_token = create_access_token(identity={
        'user': nuevo_usuario.user_id,
        'type': nuevo_usuario.role_id,
        'centrocostos': nuevo_usuario.costcenter_id,
        'email': nuevo_usuario.user_email
    })
    
    return jsonify({'token': auth_token, 'usuario': nuevo_usuario.as_dict()}), 201

@bp.route('/is-verify', methods=['GET'])
@jwt_required()
def is_verify():
    try:
        # Debugging: Verifica la información del token
        print("Token recibido:", request.headers.get('Authorization'))
        current_user = get_jwt_identity()
        return jsonify(True)
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"msg": "Invalid token"}), 401
