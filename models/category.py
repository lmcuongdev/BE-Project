from app import db
from models.base import BaseModel


class CategoryModel(BaseModel):
    __tablename__ = 'category'

    name = db.Column(db.String(50), unique=True, nullable=False)
