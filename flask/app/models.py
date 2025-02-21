from database import db

class Broker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30), unique=True, nullable=False)
    name = db.Column(db.String(30), nullable=False)
    uau = db.Column(db.String(10), nullable=False)  
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'uau': self.uau,
            'is_admin': self.is_admin
        }