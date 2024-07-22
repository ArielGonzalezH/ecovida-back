from app.extensions import db

class Sale(db.Model):
    __tablename__ = 'SALE'
    sale_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    sale_date = db.Column(db.DateTime, nullable=False)
    sale_quantity = db.Column(db.Integer, nullable=False)

    def as_dict(self):
        return {
            "sale_id": self.sale_id,
            "product_id": self.product_id,
            "user_id": self.user_id,
            "sale_date": self.sale_date,
            "sale_quantity": self.sale_quantity
        }
