from flask import Blueprint, current_app, url_for, request, make_response, redirect, session, render_template

from superform.utils import login_required, get_instance_from_module_path
from superform.models import db, Channel
import ast

channels_page = Blueprint('channels', __name__)


@channels_page.route("/channels", methods=['GET', 'POST'])
@login_required(admin_required=True)
def channel_list():
    if request.method == "POST":
        action = request.form.get('@action', '')
        if action == "new":
            name = request.form.get('name')
            module = request.form.get('module')
            if module in current_app.config["PLUGINS"].keys():
                channel = Channel(name=name, module=module, config="{}")
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
    return render_template("channels.html", channels=channels, modules=current_app.config["PLUGINS"].keys())


@channels_page.route("/configure/<int:id>", methods=['GET','POST'])
@login_required(admin_required=True)
def configure_channel(id):
    c = Channel.query.get(id)
    m = c.module
    clas = get_instance_from_module_path(m)
    config_fields = clas.CONFIG_FIELDS

    if request.method == 'GET':
        if(c.config is not ""):
            d = ast.literal_eval(c.config)
            setattr(c, "config_dict", d)
        return render_template("channel_configure.html",channel = c, config_fields = config_fields)
    str_conf="{"
    for field in config_fields:
        str_conf = str_conf+"'"+field+"' : '"+request.form.get(field)+"',"
    str_conf = str_conf+"}"
    c.config=str_conf
    db.session.commit()
    return redirect(url_for('channels.channel_list'))
