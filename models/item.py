from app import db


class ItemModel(db.Model):
    __tablename__ = 'item'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True, nullable=False)
    description = db.Column(db.String(2000), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    created_at = db.Column(db.TIMESTAMP())
    updated_at = db.Column(db.TIMESTAMP())

    category = db.relationship('CategoryModel')
    user = db.relationship('UserModel')

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, name, description, category_id):
        self.name = name
        self.description = description
        self.category_id = category_id
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
