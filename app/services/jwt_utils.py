from flask_jwt_extended import create_access_token

def generate_jwt(user_id, role_id, user_name, user_email):
    # Define el payload para el token
    payload = {
        'user': user_id,
        'type': role_id,
        'name': user_name,
        'email': user_email
    }
    
    # Crea el token JWT
    token = create_access_token(identity=payload)
    
    return token