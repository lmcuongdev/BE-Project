from app import db


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.TIMESTAMP())
    updated_at = db.Column(db.TIMESTAMP())

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, **kwargs):
        for col, val in kwargs.items():
            setattr(self, col, val)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
