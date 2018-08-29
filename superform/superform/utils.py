from datetime import datetime
from functools import wraps
from flask import render_template, session, current_app

from superform.models import Authorization, Channel


def login_required(admin_required=False):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not session.get("logged_in", False) or (admin_required and not session.get("admin", False)):
                return render_template("403.html"), 403
            else:
                return f(*args, **kwargs)
        return decorated_function
    return decorator


def datetime_converter(str):
    return datetime.strptime(str, "%Y-%m-%d")

def str_converter(datet):
    return datetime.strftime(datet,"%Y-%m-%d")

def get_instance_from_module_path(module_p):
    module_p=module_p.replace(".","/")
    import importlib.util
    spec = importlib.util.spec_from_file_location("module.name", module_p+".py")
    foo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(foo)
    return foo

def get_modules_names(modules_keys):
    return [m.split('.')[2] for m in modules_keys]

def get_module_full_name(module_name):
    for m in current_app.config["PLUGINS"].keys():
        if(m.split('.')[2] == module_name):
            return m

def get_moderate_channels_for_user(u):
    auth = Authorization.query.filter(Authorization.user_id == u.id, Authorization.permission == 2)
    chan = [Channel.query.get(a.channel_id) for a in auth]
    return chan

def is_moderator(user):
    auth = Authorization.query.filter(Authorization.user_id == user.id, Authorization.permission == 2)
    return auth.count() > 0