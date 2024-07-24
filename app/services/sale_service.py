from flask import Blueprint, request, jsonify
from extensions import db
from models.sale import Sale

bp = Blueprint('sale_service', __name__)

@bp.route('/ventas', methods=['GET'])
def obtener_ventas():
    ventas = Sale.query.all()
    return jsonify([venta.as_dict() for venta in ventas])

@bp.route('/ventas/<int:id>', methods=['GET'])
def obtener_venta(id):
    venta = Sale.query.get(id)
    return jsonify(venta.as_dict()) if venta else ('', 404)

@bp.route('/ventas', methods=['POST'])
def crear_venta():
    data = request.json

    max_id = db.session.query(db.func.max(Sale.sale_id)).scalar()
    nuevo_id = max_id + 1 if max_id is not None else 1

    nueva_venta = Sale(
        sale_id=nuevo_id,
        product_id=data['product_id'],
        user_id=data['user_id'],
        sale_date=data['sale_date'],
        sale_quantity=data['sale_quantity']
    )
    db.session.add(nueva_venta)
    db.session.commit()
    return jsonify(nueva_venta.as_dict()), 201

@bp.route('/ventas/<int:id>', methods=['PUT'])
def actualizar_venta(id):
    data = request.json
    venta = Sale.query.get(id)
    if venta:
        for key, value in data.items():
            setattr(venta, key, value)
        db.session.commit()
        return jsonify(venta.as_dict())
    else:
        return ('', 404)
    
@bp.route('/ventas/<int:id>', methods=['DELETE'])
def eliminar_venta(id):
    venta = Sale.query.get(id)
    if (venta):
        db.session.delete(venta)
        db.session.commit()
        return ('', 204)
    else:
        return ('', 404)