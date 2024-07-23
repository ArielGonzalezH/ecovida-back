from extensions import db

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
            "user_id": self.user_id,
            "role_id": self.role_id,
            "user_name": self.user_name,
            "user_lastname": self.user_lastname,
            "user_email": self.user_email,
            "user_password": self.user_password
        }