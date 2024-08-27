from flask import Blueprint, request, jsonify
from extensions import db
from models.product import Product
from rabbitmq import enviar_mensaje_a_rabbitmq
import logging
from sqlalchemy import text

bp = Blueprint('product_service', __name__)

@bp.route('/productos', methods=['GET'])
def obtener_productos():
    productos = Product.query.all()
    try:
        enviar_mensaje_a_rabbitmq('products', 'Consulta de todos los productos realizada')
    except Exception as e:
        logging.error(f"Error al enviar mensaje a RabbitMQ: {e}")
    return jsonify([producto.as_dict() for producto in productos])

@bp.route('/productos/<int:id>', methods=['GET'])
def obtener_producto(id):
    producto = Product.query.get(id)
    try:
        enviar_mensaje_a_rabbitmq('products', f'Consulta del producto con ID {id} realizada')
    except Exception as e:
        logging.error(f"Error al enviar mensaje a RabbitMQ: {e}")
    return jsonify(producto.as_dict()) if producto else ('', 404)

@bp.route('/productos', methods=['POST'])
def crear_producto():
    data = request.json

    max_id = db.session.query(db.func.max(Product.product_id)).scalar()
    nuevo_id = max_id + 1 if max_id is not None else 1

    nuevo_producto = Product(
        product_id=nuevo_id,
        found_id=data['found_id'],
        product_name=data['product_name'],
        product_price=data['product_price'],
        product_description=data['product_description'],
        product_stock=data['product_stock'],
        product_duedate=data['product_duedate']
    )
    db.session.add(nuevo_producto)
    db.session.commit()
    try:
        enviar_mensaje_a_rabbitmq('products', f'Producto creado: {nuevo_producto.as_dict()}')
    except Exception as e:
        logging.error(f"Error al enviar mensaje a RabbitMQ: {e}")
    return jsonify(nuevo_producto.as_dict()), 201

@bp.route('/productos/<int:id>', methods=['PUT'])
def actualizar_producto(id):
    data = request.json
    producto = Product.query.get(id)
    if producto:
        for key, value in data.items():
            setattr(producto, key, value)
        db.session.commit()
        try:
            enviar_mensaje_a_rabbitmq('products', f'Producto actualizado: {producto.as_dict()}')
        except Exception as e:
            logging.error(f"Error al enviar mensaje a RabbitMQ: {e}")
        return jsonify(producto.as_dict())
    else:
        return ('', 404)

@bp.route('/productos/<int:id>', methods=['DELETE'])
def eliminar_producto(id):
    producto = Product.query.get(id)
    if (producto):
        db.session.delete(producto)
        db.session.commit()
        try:
            enviar_mensaje_a_rabbitmq('products', f'Producto eliminado: {producto.as_dict()}')
        except Exception as e:
            logging.error(f"Error al enviar mensaje a RabbitMQ: {e}")
        return ('', 204)
    else:
        return ('', 404)

@bp.route('/productos/foundation/<int:found_id>', methods=['GET'])
def obtener_productos_por_foundation(found_id):
    productos = Product.query.filter_by(found_id=found_id).all()
    return jsonify([producto.as_dict() for producto in productos]) if productos else ('', 404)

@bp.route('/user_foundation_product/<int:user_id>', methods=['GET'])
def obtener_user_foundation_product(user_id):
    query = text("""
    SELECT
        U.user_id AS user_user_id,
        U.role_id AS user_role_id,
        U.user_name AS user_user_name,
        U.user_lastname AS user_user_lastname,
        U.user_email AS user_user_email,
        U.user_password AS user_user_password,
        F.found_id AS foundation_found_id,
        F.USER_ID AS foundation_user_id,
        F.found_name AS foundation_found_name,
        F.found_ruc AS foundation_found_ruc,
        P.product_id AS product_product_id,
        P.FOUND_ID AS product_found_id,
        P.product_name AS product_product_name,
        P.product_price AS product_product_price,
        P.product_description AS product_product_description,
        P.product_stock AS product_product_stock,
        P.product_duedate AS product_product_duedate
    FROM USER AS U
    LEFT JOIN FOUNDATION AS F ON U.user_id = F.user_id
    LEFT JOIN PRODUCT AS P ON F.found_id = P.found_id
    WHERE U.user_id = :user_id
    """)
    result = db.session.execute(query, {'user_id': user_id})
    
    # Convert result to a list of dictionaries
    rows = result.mappings().all()

    # Initialize the data dictionary
    data = {
        'user': None,
        'foundations': []
    }
    
    foundations_dict = {}

    for row in rows:
        # Collecting user data, setting it once since it is the same for all rows
        if not data['user']:
            data['user'] = {key: row[key] for key in row if key.startswith('user_')}
        
        # Extract foundation data
        found_id = row['foundation_found_id']
        if found_id not in foundations_dict:
            foundations_dict[found_id] = {
                'foundation': {key: row[key] for key in row if key.startswith('foundation_')},
                'products': []
            }
        
        # Extract product data if present
        product_data = {key: row[key] for key in row if key.startswith('product_')}
        if product_data and row['product_product_id'] is not None:
            foundations_dict[found_id]['products'].append(product_data)

    # Convert dictionary to list
    data['foundations'] = list(foundations_dict.values())

    return jsonify(data)
