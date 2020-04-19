from web import create_app
from flask_migrate import MigrateCommand, Manager

manager = Manager(create_app)
manager.add_command('db', MigrateCommand)
