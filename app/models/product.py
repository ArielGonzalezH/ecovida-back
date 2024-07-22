from app.extensions import db

class Product(db.Model):
    __tablename__ = 'PRODUCT'
    product_id = db.Column(db.Integer, primary_key=True)
    found_id = db.Column(db.Integer, nullable=False)
    product_name = db.Column(db.String(32), nullable=False)
    product_price = db.Column(db.Float, nullable=False)
    product_description = db.Column(db.String(255), nullable=False)
    product_stock = db.Column(db.Integer, nullable=False)
    product_duedate = db.Column(db.DateTime, nullable=False)

    def as_dict(self):
        return {
            "product_id": self.product_id,
            "found_id": self.found_id,
            "product_name": self.product_name,
            "product_price": self.product_price,
            "product_description": self.product_description,
            "product_stock": self.product_stock,
            "product_duedate": self.product_duedate
        }
