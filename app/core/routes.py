from app.core import main
from flask import redirect, session, render_template


def get_user_session_info(key):
    return session['user'].get(
        key,
        'Key `{0}` not found in user session info'.format(key)
    )


def get_user_details(fields):
    defs = [
        '<dt>{0}</dt><dd>{1}</dd>'.format(f, get_user_session_info(f))
        for f in fields
    ]
    return '<dl>{0}</dl>'.format(''.join(defs))


@main.route('/')
def index():

    if 'user' in session:
        details = get_user_details([
            'eppn',
            'uid',
            'givenName',
            'mail',
            'sn',
            'affiliation',
            'displayName',
            'title'
        ])
    else:
        details = ''
    return render_template('index.html',details=details)

@main.route('/logout')
def logout():
    session.pop('user')
    return redirect('/')
