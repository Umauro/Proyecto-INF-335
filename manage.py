import config
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from app import app,db

#here imports models
from models.games_model import Games
from models.price_model import Price
app.config.from_object(config.DevelopmentConfig)

migrate = Migrate(app,db,compare_type = True)
manager = Manager(app)

manager.add_command('db',MigrateCommand)


if __name__ == '__main__':
    manager.run()
