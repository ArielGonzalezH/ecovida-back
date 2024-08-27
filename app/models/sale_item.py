from extensions import db

class Sale_Item(db.Model):
    __tablename__ = 'SALE_ITEMS'
    item_id = db.Column(db.Integer, primary_key=True)
    sale_header_id = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    item_quantity = db.Column(db.Integer, nullable=False)

    def as_dict(self):
        return {
            "item_id": self.item_id,
            "sale_header_id": self.sale_header_id,
            "product_id": self.product_id,
            "item_quantity": self.item_quantity
        }
