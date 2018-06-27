import os
from flask import Flask, session, redirect
from flask_bootstrap import Bootstrap
from flask_sso import SSO
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
ext = SSO()
bo = Bootstrap()

def create_app(config_type="dev"):
    app = Flask(__name__)
    
    SSO_ATTRIBUTE_MAP = {
        'eppn': (True, 'eppn'),  # dhf8r@virginia.edu
        'uid': (False, 'uid'),  # dhf8r
        'givenName': (False, 'givenName'),  # Daniel
        'mail': (False, 'email'),  # dhf8r@Virginia.EDU
        'sn': (False, 'surName'),  # Funk
        'affiliation': (False, 'affiliation'),  # 'staff@virginia.edu;member@virginia.edu'
        'displayName': (False, 'displayName'),  # Daniel Harold Funk
        'title': (False, 'title')  # SOFTWARE ENGINEER V
    }
    
    app.config.setdefault('SSO_ATTRIBUTE_MAP', SSO_ATTRIBUTE_MAP)
    app.config.setdefault('SSO_LOGIN_URL', '/login')
    

    ext.init_app(app)
    
    @ext.login_handler
    def login(user_info):
        session['user'] = user_info
        return redirect('/')


    bo.init_app(app)
    
    configuration = os.path.join(os.getcwd(), 'config', str(config_type) + '.py')
    app.config.from_pyfile(configuration)
    
    db.init_app(app)
    
    # import blueprint
    from app.core import main
    app.register_blueprint(main)
    return app


def wsgi(*args, **kwargs):
    return create_app()(*args, **kwargs)
