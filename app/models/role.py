from extensions import db

class Role(db.Model):
    __tablename__ = 'ROLE'
    role_id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(32), nullable=False)

    def as_dict(self):
        return {
            "role_id": self.role_id,
            "role_name": self.role_name
        }