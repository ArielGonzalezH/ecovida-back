from flask import Blueprint, request, jsonify
from extensions import db
from models.foundation import Foundation

bp = Blueprint('foundation_service', __name__)

@bp.route('/test', methods=['GET'])
def test_route():
    return 'Hello World'

@bp.route('/foundations', methods=['GET'])
def get_foundations():
    foundations = Foundation.query.all()
    return jsonify([foundation.as_dict() for foundation in foundations])

@bp.route('/foundations/<int:id>', methods=['GET'])
def get_foundation(id):
    foundation = Foundation.query.get(id)
    return jsonify(foundation.as_dict()) if foundation else ('', 404)

@bp.route('/foundations', methods=['POST'])
def create_foundation():
    try:
        data = request.json

        # Obtener el ID más alto en la base de datos
        max_id = db.session.query(db.func.max(Foundation.found_id)).scalar()
        new_id = max_id + 1 if max_id is not None else 1

        # Crear nueva fundación con el nuevo ID
        new_foundation = Foundation(found_id=new_id, **data)
        
        db.session.add(new_foundation)
        db.session.commit()
        
        return jsonify(new_foundation.as_dict()), 201
    except Exception as e:
        print(f"Error al crear fundación: {e}")
        return jsonify({'error': str(e)}), 500

@bp.route('/foundations/<int:id>', methods=['PUT'])
def update_foundation(id):
    data = request.json
    foundation = Foundation.query.get(id)
    if foundation:
        for key, value in data.items():
            setattr(foundation, key, value)
        db.session.commit()
        return jsonify(foundation.as_dict())
    else:
        return ('', 404)
    
@bp.route('/foundations/<int:id>', methods=['DELETE'])
def delete_foundation(id):
    foundation = Foundation.query.get(id)
    if (foundation):
        db.session.delete(foundation)
        db.session.commit()
        return ('', 204)
    else:
        return ('', 404)