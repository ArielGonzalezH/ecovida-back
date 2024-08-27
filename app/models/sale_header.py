from extensions import db

class Sale_Header(db.Model):
    __tablename__ = 'SALE_HEADER'
    sh_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    sale_date = db.Column(db.DateTime, nullable=False)
    sale_sub = db.Column(db.Float, nullable=False)
    sale_IVA = db.Column(db.Float, nullable=False)
    sale_total = db.Column(db.Float, nullable=False)

    def as_dict(self):
        return {
            "sh_id": self.sh_id,
            "user_id": self.user_id,
            "sale_date": self.sale_date,
            "sale_sub": self.sale_sub,
            "sale_IVA": self.sale_IVA,
            "sale_total": self.sale_total
        }