from extensions import db

class Package(db.Model):
    __tablename__ = 'PACKAGE'
    package_id = db.Column(db.Integer, primary_key=True)
    sale_header_id = db.Column(db.Integer, nullable=False)
    state_package = db.Column(db.String(35), nullable=False)
    date_verification = db.Column(db.DateTime)
    date_shipping = db.Column(db.DateTime)
    date_delivery = db.Column(db.DateTime)


    def as_dict(self):
        return {
            "package_id": self.package_id,
            "sale_header_id": self.sale_header_id,
            "state_package": self.state_package,
            "date_verification": self.date_verification,
            "date_shipping": self.date_shipping,
            "date_delivery": self.date_delivery
        }
