import ast
import datetime

from flask import Blueprint, current_app, url_for, request, redirect, \
    render_template

from superform.models import db, Channel
from superform.plugins.LinkedIn import linkedin_plugin, linkedin_use
from superform.utils import login_required, get_instance_from_module_path, \
    get_modules_names, get_module_full_name

channels_page = Blueprint('channels', __name__)

"""
    Final static variables for the cookies keys related to the LinkedIn 
    plugin.
"""
LAST_ACCESS_TOKEN = "last_access_token"
LAST_CREATION_TIME = "last_creation_time"
LAST_CHANNEL_ID = "last_channel_id"


@channels_page.route("/channels", methods = ['GET', 'POST'])
@login_required(admin_required = True)
def channel_list():
    if request.method == "POST":
        action = request.form.get('@action', '')
        if action == "new":
            name = request.form.get('name')
            module = request.form.get('module')
            if module in get_modules_names(
                    current_app.config["PLUGINS"].keys()):
                channel = Channel(name = name,
                                  module = get_module_full_name(module),
                                  config = "{}")
                db.session.add(channel)
                db.session.commit()
        elif action == "delete":
            channel_id = request.form.get("id")
            channel = Channel.query.get(channel_id)
            if channel:
                db.session.delete(channel)
                db.session.commit()
        elif action == "edit":
            channel_id = request.form.get("id")
            channel = Channel.query.get(channel_id)
            name = request.form.get('name')
            channel.name = name
            db.session.commit()

    channels = Channel.query.all()
    return render_template("channels.html", channels = channels,
                           modules = get_modules_names(
                               current_app.config["PLUGINS"].keys()))


@channels_page.route("/configure/<int:id>", methods = ['GET', 'POST'])
@login_required(admin_required = True)
def configure_channel(id):
    c = Channel.query.get(id)
    m = c.module
    clas = get_instance_from_module_path(m)
    config_fields = clas.CONFIG_FIELDS

    print("This is the request.url : " + request.url)

    if request.method == 'GET':
        if c.config is not "":
            d = ast.literal_eval(c.config)
            setattr(c, "config_dict", d)
            if str(m) == "superform.plugins.LinkedIn":
                return linkedin_plugin(id, c, m, clas, config_fields)
            #
        return render_template("channel_configure.html", channel = c,
                               config_fields = config_fields)
    str_conf = "{"
    cfield = 0
    for field in config_fields:
        if cfield > 0:
            str_conf += ","
        str_conf += "\"" + field + "\" : \"" + request.form.get(field) + "\""
        cfield += 1

    """
        If any LinkedIn session cookie is present we add them to the 
        data-base.
    """
    last_access_token = request.cookies.get(LAST_ACCESS_TOKEN)
    last_creation_time = request.cookies.get(LAST_CREATION_TIME)
    last_chanel_id = request.cookies.get(LAST_CHANNEL_ID)
    if str(m) == "superform.plugins.LinkedIn" and str(last_chanel_id) == str(
            id) and last_access_token is not None and last_creation_time is not None:
        print("je suis dans la boucle")
        str_conf += ","
        str_conf += "\"" + "token" + "\" : \"" + last_access_token + "\""
        str_conf += ","
        str_conf += "\"" + "creationTime" + "\" : \"" + last_creation_time + "\""
        cfield = cfield + 2
    str_conf += "}"
    c.config = str_conf
    db.session.commit()
    return redirect(url_for('channels.channel_list'))


@channels_page.route("/configure/linkedin", methods = ['GET', 'POST'])
@login_required(admin_required = True)
def linkedin_return():
    """
        Redirected route manager for the LinkedIn plugin, sets the necessary
        cookies to continue the session.
    """
    ref = request.url
    code = ""
    if ref.startswith("http://localhost:5000/configure/linkedin?code"):
        i = ref.find("state", 46)
        code = ref[46:i - 1]
        ch_id = ref[i + 9:ref.find("rest")]
        print('The id is: ' + ch_id)
        last_access_token = linkedin_use(code)  # return from LinkedIn
        now = datetime.datetime.now()
        last_creation_time = now.strftime("%Y-%m-%d %H:%M")
        last_channel_id = ch_id
        if last_access_token is None:
            print("no token !")

    resp = redirect(url_for('channels.configure_channel', id = ch_id))
    resp.set_cookie(LAST_ACCESS_TOKEN, last_access_token.access_token)
    resp.set_cookie(LAST_CHANNEL_ID, last_channel_id)
    resp.set_cookie(LAST_CREATION_TIME, last_creation_time)
    return resp
