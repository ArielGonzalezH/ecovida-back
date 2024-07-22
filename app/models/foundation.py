from app.extensions import db

class Foundation(db.Model):
    __tablename__ = 'FOUNDATION'
    found_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    found_name = db.Column(db.String(64), nullable=False)
    found_ruc = db.Column(db.String(16), nullable=False)

    def as_dict(self):
        return {
            "found_id": self.found_id,
            "user_id": self.user_id,
            "found_name": self.found_name,
            "found_ruc": self.found_ruc
        }
