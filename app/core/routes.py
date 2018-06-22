from app.core import main


@main.route('/')
def index():
    return 'hello world!!!'
