from flask import Flask, request, make_response, jsonify, abort
from flask import render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///foo.db'
db = SQLAlchemy(app)


from models import Category, Post
from serializers import CategorySerializer, PostSerializer


@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/category', methods=['GET', 'POST'])
def category_list():
    if request.method == 'GET':
        categories = Category.query.all()
        serializer = CategorySerializer(categories)
        return serializer.data
    elif request.method == 'POST':
        name = request.form.get("name", False)
        new_category = Category(name=name)
        db.session.add(new_category)
        db.session.commit()
        serializer = CategorySerializer(new_category)
        return serializer.data


@app.route('/category/<int:category_id>', methods=['GET', 'PUT', 'DELETE'])
def category_detail(category_id):
    if request.method == 'GET':
        category = Category.query.get(category_id)
        if category is None:
            abort(404, description="Resource not found")
        serializer = CategorySerializer(category)
        return serializer.data
    elif request.method == 'PUT':
        category = Category.query.get(category_id)
        category.name = request.form['name']
        db.session.commit()
        serializer = CategorySerializer(category)
        return serializer.data
    elif request.method == 'DELETE':
        category = Category.query.get(category_id)
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
        posts = category.posts
        serializer = PostSerializer(posts)
        return serializer.data
    elif request.method == 'POST':
        category = Category.query.get(category_id)
        if category is None:
            abort(404, description="Resource not found")
        title = request.form.get("title", False)
        body = request.form.get("body", False)
        url = request.form.get("url", False)
        image_url = request.form.get("image_url", False)
        iframe = request.form.get("iframe", False)
        new_post = Post(category=category, title=title, body=body, url=url, image_url=image_url, iframe=iframe)
        category.posts.append(new_post)
        db.session.commit()
        serializer = PostSerializer(new_post)
        return serializer.data


@app.route('/category/<int:category_id>/post/<int:post_id>', methods=['GET', 'PUT', 'DELETE'])
def post_detail(category_id, post_id):
    if request.method == 'GET':
        category = Category.query.get(category_id)
        if category is None:
            abort(404, description="Resource not found")
        try:
            post = category.posts[post_id]
            serializer = PostSerializer(post)
            return serializer.data
        except IndexError:
            abort(404, description="Resource not found")
    elif request.method == 'PUT':
        category = Category.query.get(category_id)
        if category is None:
            abort(404, description="Resource not found")
        try:
            post = category.posts[post_id]
            post.title = request.form.get("title", False)
            post.body = request.form.get("body", False)
            post.url = request.form.get("url", False)
            post.image_url = request.form.get("image_url", False)
            post.iframe = request.form.get("iframe", False)
            db.session.commit()
            serializer = PostSerializer(post)
            return serializer.data
        except IndexError:
            abort(404, description="Resource not found")
    elif request.method == 'DELETE':
        category = Category.query.get(category_id)
        if category is None:
            abort(404, description="Resource not found")
        try:
            post = category.posts[post_id]
            db.session.delete(post)
            db.session.commit()
            return make_response(jsonify({}), 204)
        except IndexError:
            abort(404, description="Resource not found")


if __name__ == '__main__':
    app.run()
