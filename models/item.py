from app import db
from models.base import BaseModel


class ItemModel(BaseModel):
    __tablename__ = 'item'

    name = db.Column(db.String(200), unique=True, nullable=False)
    description = db.Column(db.String(2000), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer,
                            db.ForeignKey('category.id'),
                            nullable=False)

    category = db.relationship('CategoryModel')
    user = db.relationship('UserModel')
