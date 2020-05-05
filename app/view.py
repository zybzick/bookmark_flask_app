from flask import request, make_response, jsonify, abort, render_template
from app import app, db
from app.models import Category, Post
from app.utilits import autoget
from app.serializers import CategorySerializer, PostSerializer
from sqlalchemy import desc


@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/category', methods=['GET', 'POST'])
def category_list():
    if request.method == 'GET':
        # categories = Category.query.order_by(desc())[::-1]
        categories = Category.query.order_by(desc(Category.id)).all()
        serializer = CategorySerializer(categories)
        return serializer.data
    elif request.method == 'POST':
        name = request.json.get("name")
        new_category = Category(name=name)
        db.session.add(new_category)
        db.session.commit()
        return CategorySerializer(new_category).data


@app.route('/category/<int:category_id>', methods=['GET', 'PUT', 'DELETE'])
def category_detail(category_id):
    if request.method == 'GET':
        category = Category.query.get(category_id)
        if category is None:
            abort(404, description="Resource not found")
        return CategorySerializer(category).data
    elif request.method == 'PUT':
        category = Category.query.get(category_id)
        if category is None:
            abort(404, description="Resource not found")
        category.name = request.json['name']
        db.session.commit()
        return CategorySerializer(category).data
    elif request.method == 'DELETE':
        category = Category.query.get(category_id)
        print(category)
        if category is None:
            abort(404, description="Resource not found")
        db.session.delete(category)
        db.session.commit()
        response = make_response(jsonify({}), 204)
        return response


@app.route('/category/<int:category_id>/post', methods=['GET', 'POST'])
def post_list(category_id):
    if request.method == 'GET':
        category = Category.query.get(category_id)
        if category is None:
            abort(404, description="Resource not found")
        posts = category.posts[::-1]
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


@app.route('/category/<int:category_id>/post/<int:post_id>', methods=['GET', 'PUT', 'DELETE'])
def post_detail(category_id, post_id):
    if request.method == 'GET':
        try:
            post = Post.query.get(post_id)
            serializer = PostSerializer(post)
            return serializer.data
        except (IndexError, AttributeError):
            abort(401, description="Resource not found")
    elif request.method == 'PUT':
        try:
            post = Post.query.get(post_id)
            post.title, post.body, post.url, post.image_url, post.iframe = autoget(['title', 'body', 'url', 'image_url', 'iframe'], request.json)
            db.session.commit()
            return PostSerializer(post).data
        except (IndexError, AttributeError):
            abort(404, description="Resource not found")
    elif request.method == 'DELETE':
        try:
            post = Post.query.get(post_id)
            db.session.delete(post)
            db.session.commit()
            return make_response(jsonify({}), 204)
        except (IndexError, AttributeError):
            abort(404, description="Resource not found")