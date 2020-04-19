from flask_migrate import MigrateCommand
from flask_script import Manager
from web import create_app

app = create_app()
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    manager.run()
    db.create_all()
