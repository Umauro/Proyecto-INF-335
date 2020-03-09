import config 

from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
api = Api(app)
db = SQLAlchemy(app)

app.config.from_object(config.DevelopmentConfig)

#Here import endpoints
from endpoint.games_resource import GamesResource
api.add_resource(GamesResource,'/games','/games/<string:permalink>')


if __name__ == '__main__':
    app.run()