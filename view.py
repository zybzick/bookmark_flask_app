from flask import request, make_response, jsonify, abort, render_template, Blueprint
from models import db
from models import Category, Post
from utilits import autoget
from serializers import CategorySerializer, PostSerializer


my_view = Blueprint('my_view', __name__)


@my_view.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404


@my_view.route('/')
def index():
    return render_template('index.html')


@my_view.route('/category', methods=['GET', 'POST'])
def category_list():
    if request.method == 'GET':
        categories = Category.query.all()
        serializer = CategorySerializer(categories)
        return serializer.data
    elif request.method == 'POST':
        name = request.json.get("name")
        new_category = Category(name=name)
        db.session.add(new_category)
        db.session.commit()
        return CategorySerializer(new_category).data


@my_view.route('/category/<int:category_id>', methods=['GET', 'PUT', 'DELETE'])
def category_detail(category_id):
    if request.method == 'GET':
        category = Category.query.get(category_id)
        if category is None:
            abort(404, description="Resource not found")
        return CategorySerializer(category).data
    elif request.method == 'PUT':
        category = Category.query.get(category_id)
        category.name = request.json['name']
        db.session.commit()
        return CategorySerializer(category).data
    elif request.method == 'DELETE':
        category = Category.query.get(category_id)
        if category is None:
            abort(404, description="Resource not found")
        db.session.delete(category)
        db.session.commit()
        response = make_response(jsonify({}), 204)
        return response


@my_view.route('/category/<int:category_id>/post', methods=['GET', 'POST'])
def post_list(category_id):
    if request.method == 'GET':
        category = Category.query.get(category_id)
        if category is None:
            abort(404, description="Resource not found")
        posts = category.posts
        return PostSerializer(posts).data
    elif request.method == 'POST':
        category = Category.query.get(category_id)
        if category is None:
            abort(404, description="Resource not found")
        title, body, url, image_url, iframe = autoget(['title', 'body', 'url', 'image_url', 'iframe'], request.json)
        new_post = Post(category=category, title=title, body=body, url=url, image_url=image_url, iframe=iframe)
        category.posts.append(new_post)
        db.session.commit()
        return PostSerializer(new_post).data


@my_view.route('/category/<int:category_id>/post/<int:post_id>', methods=['GET', 'PUT', 'DELETE'])
def post_detail(category_id, post_id):
    if request.method == 'GET':
        category = Category.query.get(category_id)
        try:
            post = category.posts[post_id]
            serializer = PostSerializer(post)
            return serializer.data
        except (IndexError, AttributeError):
            abort(401, description="Resource not found")
    elif request.method == 'PUT':
        category = Category.query.get(category_id)
        try:
            post = category.posts[post_id]
            post.title, post.body, post.url, post.image_url, post.iframe = autoget(['title', 'body', 'url', 'image_url', 'iframe'], request.json)
            db.session.commit()
            return PostSerializer(post).data
        except (IndexError, AttributeError):
            abort(404, description="Resource not found")
    elif request.method == 'DELETE':
        category = Category.query.get(category_id)
        try:
            post = category.posts[post_id]
            db.session.delete(post)
            db.session.commit()
            return make_response(jsonify({}), 204)
        except (IndexError, AttributeError):
            abort(404, description="Resource not found")