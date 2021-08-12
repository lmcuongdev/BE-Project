from app import db
from models.base_model import BaseModel


class UserModel(BaseModel):
    __tablename__ = 'user'

    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.CHAR(60), nullable=False)

    @classmethod
    def has_username(cls, username):
        return cls.find_by_username(username) is not None

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()
