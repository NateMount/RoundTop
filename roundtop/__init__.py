# [ Src Init - RoundTop ]

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import roundtop.config as config

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.DB_URI
app.config['SECRET_KEY'] = config.SECRET

db = SQLAlchemy(app)

from roundtop import routes