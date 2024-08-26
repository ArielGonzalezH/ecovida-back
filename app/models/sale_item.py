from extensions import db

class Sale_Item(db.Model):
    __tablename__ = 'SALE_ITEM'
    item_id = db.Column(db.Integer, primary_key=True)
    sale_header_id = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    sale_quantity = db.Column(db.Integer, nullable=False)

    def as_dict(self):
        return {
            "item_id": self.item_id,
            "sale_header_id": self.sale_header_id,
            "product_id": self.product_id,
            "sale_quantity": self.sale_quantity
        }
