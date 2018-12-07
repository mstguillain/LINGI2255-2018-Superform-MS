import ast
import datetime
import time

from flask import Blueprint, current_app, url_for, request, redirect, \
    render_template

from superform.models import db, Channel
from superform.plugins.LinkedIn import linkedin_plugin, \
    linkedin_code_processing
from superform.plugins.pdf import pdf_plugin
from superform.utils import login_required, get_instance_from_module_path, \
    get_modules_names, get_module_full_name

channels_page = Blueprint('channels', __name__)

# author: Team 06
# date: December 2018
# Final static variables for the cookies keys related to the LinkedIn plugin.
LAST_ACCESS_TOKEN = "last_access_token"
LAST_CREATION_TIME = "last_creation_time"
LAST_CHANNEL_ID = "last_channel_id"
LAST_STATUS = "0"


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
    if request.method == 'GET':
        if c.config is not "":
            d = ast.literal_eval(c.config)
            setattr(c, "config_dict", d)
            if str(m) == "superform.plugins.LinkedIn":
                last_status = request.cookies.get(LAST_STATUS)
                return linkedin_plugin(id, c, config_fields, last_status)
            if str(m) == 'superform.plugins.pdf':
                return pdf_plugin(id, c, config_fields)

        return render_template("channel_configure.html", channel = c,
                               config_fields = config_fields)
    str_conf = "{"
    cfield = 0
    for field in config_fields:
        if cfield > 0:
            str_conf += ","
        str_conf += "\"" + field + "\" : \"" + request.form.get(field) + "\""
        cfield += 1

    # If any LinkedIn session cookie is present we add them to the
    # data-base.

    last_access_token = request.cookies.get(LAST_ACCESS_TOKEN)
    last_creation_time = request.cookies.get(LAST_CREATION_TIME)
    last_channel_id = request.cookies.get(LAST_CHANNEL_ID)

    print("Saving LinkedIn channel data")
    if str(m) == "superform.plugins.LinkedIn" and str(last_channel_id) == str(
            id) and last_access_token is not None and last_creation_time is not None:
        if cfield > 0:
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
        author: Team 06
        date: December 2018
        Redirected route manager for the LinkedIn plugin, sets the necessary
        cookies to continue the session.
    """
    print("Redirected from LinkedIn")
    url = request.url
    if url.startswith(request.url_root + "configure/linkedin?code"):
        i = url.find("state", 46)
        code = url[46:i - 1]
        print("Code retrieved")
        ch_id = url[i + 9:url.find("rest")]
        last_access_token = linkedin_code_processing(
            code)  # return from LinkedIn
        now = datetime.datetime.now()
        last_creation_time = str(int(
            time.time()))  # str(time.gmtime()) #now.strftime("%Y-%m-%d %H:%M")
        last_channel_id = ch_id
        if last_access_token is None:
            print("No token retrieved!")

        redirection = redirect(
            url_for('channels.configure_channel', id = ch_id))
        redirection.set_cookie(LAST_ACCESS_TOKEN,
                               last_access_token.access_token)
        redirection.set_cookie(LAST_CHANNEL_ID, last_channel_id)
        redirection.set_cookie(LAST_CREATION_TIME, last_creation_time)
        redirection.set_cookie(LAST_STATUS, "1:%s" % ch_id)
    elif url.startswith(
            request.url_root + "configure/linkedin?error=user_cancelled_authorize"):
        print("Error: authorization cancelled")
        i = url.find("state")
        ch_id = url[i + 9:url.find("rest")]
        redirection = redirect(
            url_for('channels.configure_channel', id = ch_id))
        redirection.set_cookie(LAST_STATUS, "-1:%s" % ch_id)
    else:
        print("Error: no code found")
        i = url.find("state")
        ch_id = url[i + 9:url.find("rest")]
        redirection = redirect(
            url_for('channels.configure_channel', id = ch_id))
        redirection.set_cookie(LAST_STATUS, "-1:%s" % ch_id)
    return redirection
