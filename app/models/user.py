from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'USER'
    user_id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer, nullable=False)
    user_name = db.Column(db.String(64), nullable=False)
    user_lastname = db.Column(db.String(64), unique=True, nullable=False)
    user_email = db.Column(db.String(128), unique=True, nullable=False)
    user_password = db.Column(db.String(255), nullable=False)
    
    def as_dict(self):
        return {
            "user_id": int(self.user_id), 
            "role_id": int(self.role_id),
            "user_name": self.user_name,
            "user_lastname": self.user_lastname,
            "user_email": self.user_email
        }
    
    def set_password(self, password):
        self.user_password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.user_password, password)
