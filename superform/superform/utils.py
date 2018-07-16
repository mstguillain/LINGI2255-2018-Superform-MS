from functools import wraps
from flask import render_template, session


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