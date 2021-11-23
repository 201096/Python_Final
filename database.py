from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456789@localhost:5432/CoinData'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class News(db.Model):
    __tablename__ = 'news'
    id = db.Column(db.Integer, primary_key=True)
    name_of_coin = db.Column( db.VARCHAR(255))
    news = db.Column( db.VARCHAR(5000))


    def __init__(self,id,name_of_coin, news):
        self.id = id
        self.name_of_coin = name_of_coin
        self.news = news