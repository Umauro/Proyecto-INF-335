from flask import request
from flask_restful import Resource
from flask_restful import marshal, fields
from app import db
from sqlalchemy.sql.expression import func

from models.games_model import Games


price_fields = {
    'date':fields.DateTime,
    'price':fields.Integer
}

games_fields = {
    'permalink': fields.String,
    'title': fields.String,
    'price': fields.Integer,
    'image': fields.String,
    'url': fields.String,
    'description': fields.String,
    'prices': fields.Nested(price_fields)
}

response_fields = {
    'status': fields.Integer,
    'data': fields.Raw
}

class GamesResource(Resource):
    def get(self,permalink=None):
        try:
            if permalink == None:
                games_list = Games.query.order_by(func.random()).limit(20).all()
                if not len(games_list):
                    raise Exception('No hay juegos disponibles')
                return marshal({'status':1,'data':[marshal(data,games_fields) for data in games_list]},response_fields)
            else:
                game = Games.query.filter(Games.permalink == permalink).first()
                if not game:
                    raise Exception('No existe el juego')
                return marshal({'status':1,'data':marshal(game,games_fields)},response_fields)
        except Exception as error:
            return marshal({'status':0,'data':{'error':str(error)}},response_fields)
