from . import db
from flask import json

class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    products  = db.Column(db.Text, unique=False, nullable=False)
    amount = db.Column(db.Numeric, unique=False, nullable=False)
    created_at = db.Column(db.DateTime, unique=False, nullable=False)
    updated_at = db.Column(db.DateTime, unique=False, nullable=False)
    status = db.Column(db.String(255), unique=False, nullable=False)

    def __repr__(self):
        return f"<Order id={self.id!r}>"

    @property
    def serialized(self):
        return {
            'id': self.id ,
            'products': json.loads(self.products),
            'amount': self.amount,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'status': self.status,
        }
