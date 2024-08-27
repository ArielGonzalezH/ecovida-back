from flask import Blueprint, request, jsonify
from extensions import mongo  # Importar mongo desde extensions
from models.mongo_comment_model import Comment
from bson import ObjectId  # Importar ObjectId para manejarlo en la conversión

bp = Blueprint('comment_service', __name__)

# Función auxiliar para convertir ObjectId a string en los documentos
def comment_serializer(comment):
    comment['_id'] = str(comment['_id'])
    return comment

@bp.route('/comentarios', methods=['POST'])
def agregar_comentario():
    data = request.json
    producto_id = data.get('product_id')
    usuario_id = data.get('user_id')
    comentario_texto = data.get('comment_text')

    if not all([producto_id, usuario_id, comentario_texto]):
        return jsonify({"error": "Faltan campos requeridos"}), 400

    comentario = Comment(
        product_id=producto_id,
        user_id=usuario_id,
        comment_text=comentario_texto
    )

    # Insertar el comentario en la base de datos y obtener el ID insertado
    result = mongo.db.comments.insert_one(comentario.as_dict())
    comentario_id = result.inserted_id

    # Obtener el comentario recién insertado para devolverlo
    comentario = mongo.db.comments.find_one({"_id": comentario_id})
    comentario_serializado = comment_serializer(comentario)

    return jsonify(comentario_serializado), 201

@bp.route('/comentarios/<int:product_id>', methods=['GET'])
def obtener_comentarios_por_producto(product_id):
    comentarios = mongo.db.comments.find({"product_id": product_id})
    comentarios_serializados = [comment_serializer(comment) for comment in comentarios]
    return jsonify(comentarios_serializados), 200