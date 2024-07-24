from functools import wraps
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity

jwt = JWTManager()  # Instancia JWTManager

def jwt_required_with_payload(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        # Verifica el JWT
        jwt_required()
        user = get_jwt_identity()  # Obtiene el payload del token
        return fn(*args, **kwargs, user=user)
    return wrapper
