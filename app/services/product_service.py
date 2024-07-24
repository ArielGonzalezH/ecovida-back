from flask import Blueprint, request, jsonify
from extensions import db
from models.product import Product

bp = Blueprint('product_service', __name__)

@bp.route('/productos', methods=['GET'])
def obtener_productos():
    productos = Product.query.all()
    return jsonify([producto.as_dict() for producto in productos])

@bp.route('/productos/<int:id>', methods=['GET'])
def obtener_producto(id):
    producto = Product.query.get(id)
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
    return jsonify(nuevo_producto.as_dict()), 201

@bp.route('/productos/<int:id>', methods=['PUT'])
def actualizar_producto(id):
    data = request.json
    producto = Product.query.get(id)
    if producto:
        for key, value in data.items():
            setattr(producto, key, value)
        db.session.commit()
        return jsonify(producto.as_dict())
    else:
        return ('', 404)

@bp.route('/productos/<int:id>', methods=['DELETE'])
def eliminar_producto(id):
    producto = Product.query.get(id)
    if (producto):
        db.session.delete(producto)
        db.session.commit()
        return ('', 204)
    else:
        return ('', 404)
