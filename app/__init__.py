import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

def create_app(config_type):
    app = Flask(__name__)
    print(config_type)
    configuration = os.path.join(os.getcwd(),'config',str(config_type)+'.py')
    print(configuration)
    app.config.from_pyfile(configuration)

    db.init_app(app)

    #import blueprint
    from app.core import main
    app.register_blueprint(main)

    return app