from flask import Blueprint, current_app, url_for, request, make_response, redirect, session, render_template

from superform.utils import login_required
from superform.models import db, Channel, Authorization, Permission

authorizations_page = Blueprint('authorizations', __name__)


@authorizations_page.route("/authorizations", methods=['GET', 'POST'])
@login_required()
def authorizations():
    if request.method == "GET":
        if session["admin"]:
            rw_channels = Channel.query.all()
            ro_channels = []
        else:
            channels = Channel.query.join(Authorization).filter(Authorization.user_id == session["user_id"])
            rw_channels = Channel.query.join(Authorization).filter(Authorization.user_id == session["user_id"]).filter(
                Authorization.permission == Permission.MODERATOR.value)
            ro_channels = Channel.query.join(Authorization).filter(Authorization.user_id == session["user_id"]).filter(
                Authorization.permission == Permission.AUTHOR.value)
        return render_template("authorizations.html", rw_channels=rw_channels, ro_channels=ro_channels,
                               permissions=Permission)
    elif request.method == "POST":
        i = 0
        while i < (round(len(request.form) / 3)):
            user_id = request.form.get('username' + str(i))
            print(user_id)
            if user_id is not "":
                channel_id = request.form.get('channel_id'+str(i))
                print(channel_id)
                permission = request.form.get('permission' + str(i))
                print(permission)
                a = Authorization(channel_id=channel_id, user_id=user_id, permission=permission)
                db.session.add(a)
            i = i + 1

        edit_list = [[elem,elem.split('#')] for elem in request.form if elem.startswith("permission_edit")]
        print(edit_list)
        for e in edit_list:
            auth = request.form.get(e[0])
            chan_id = e[1][2]
            user= e[1][1]
            a = Authorization.query.filter(Authorization.user_id == user, Authorization.channel_id == chan_id).first()
            a.permission = auth
        db.session.commit()
        return redirect(url_for('authorizations.authorizations'))

@authorizations_page.route("/delete_auto/<string:id>/<string:cid>")
@login_required()
def delete_authorization(id,cid):
    auth = Authorization.query.filter(Authorization.user_id==id,Authorization.channel_id==cid).first()
    db.session.delete(auth)
    db.session.commit()
    return redirect(url_for('authorizations.authorizations'))
