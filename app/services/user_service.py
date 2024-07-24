from flask import Blueprint, request, jsonify
from extensions import db
from models.user import User
import jwt
import datetime
from functools import wraps
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint('user_service', __name__)

def encode_auth_token(user_id):
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
    except Exception as e:
        return str(e)

def decode_auth_token(auth_token):
    try:
        payload = jwt.decode(auth_token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'

def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return ('', 401)
        if token.startswith('Bearer '):
            token = token[7:]
        user_id = decode_auth_token(token)
        if isinstance(user_id, str):
            return ('', 401)
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/usuarios', methods=['GET'])
@token_required
def obtener_usuarios():
    usuarios = User.query.all()
    return jsonify([usuario.as_dict() for usuario in usuarios])

@bp.route('/usuarios/<int:id>', methods=['GET'])
@token_required
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
    
    auth_token = encode_auth_token(nuevo_usuario.user_id)
    return jsonify({'token': auth_token, 'usuario': nuevo_usuario.as_dict()}), 201

@bp.route('/usuarios/<int:id>', methods=['PUT'])
@token_required
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
@token_required
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
    if usuario and usuario.check_password(data['user_password']):
        auth_token = encode_auth_token(usuario.user_id)
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
    auth_token = encode_auth_token(nuevo_usuario.user_id)
    return jsonify({'token': auth_token, 'usuario': nuevo_usuario.as_dict()}), 201
