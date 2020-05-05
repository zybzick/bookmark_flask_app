from flask_sqlalchemy import SQLAlchemy
from app import db


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<Category name={self.name}, id={self.id}>'


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    body = db.Column(db.Text)
    url = db.Column(db.Text)
    image_url = db.Column(db.Text)
    iframe = db.Column(db.Text)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', backref=db.backref('posts', lazy=True, cascade="all,delete"))

    def __repr__(self):
        return f'<Post title={self.title}, catId={self.category_id}>'






