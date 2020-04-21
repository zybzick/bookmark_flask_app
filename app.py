from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from view import my_view


app = Flask(__name__)
app.register_blueprint(my_view)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///foo.db'
db = SQLAlchemy(app)

if __name__ == '__main__':
    app.run()
