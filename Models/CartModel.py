from . import db
from flask import json

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(255), unique=False, nullable=False)
    content = db.Column(db.Text, unique=False, nullable=False)
    created_at = db.Column(db.DateTime, unique=False, nullable=False)
    updated_at = db.Column(db.DateTime, unique=False, nullable=False)

    def __repr__(self):
        return f"<Cart id={self.id} code={self.code!r}>"

    @property
    def serialized(self):
        return {
            'id': self.id ,
            'code': self.code,
            'products': json.loads(self.content),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }
