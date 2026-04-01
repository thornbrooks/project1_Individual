from . import db

class Property(db.Model):
    __tablename__ = 'properties'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    num_bedrooms = db.Column(db.Integer, nullable=False)
    num_bathrooms = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(255), nullable=False)
    price = db.Column(db.String(100), nullable=False)
    property_type = db.Column(db.String(50), nullable=False)
    photo = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<Property {self.title}>'
