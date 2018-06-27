from app import create_app

if __name__=='__main__':
    env = 'dev'
    flask_app = create_app(env)
    flask_app.env=env
    flask_app.debug=True
    flask_app.run()