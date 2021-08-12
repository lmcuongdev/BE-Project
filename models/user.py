from app import db


class UserModel(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.CHAR(60), nullable=False)
    created_at = db.Column(db.TIMESTAMP())

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def has_username(cls, username):
        return cls.query.filter_by(username=username).count() > 0

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()
