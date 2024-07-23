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
    nueva_venta = Sale(**data)
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