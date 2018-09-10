from flask import Blueprint, url_for, request, redirect, render_template


from superform.utils import login_required, datetime_converter
from superform.models import db,Publishing

pub_page = Blueprint('publishings', __name__)
@pub_page.route('/moderate/<int:id>/<string:idc>',methods=["GET","POST"])
@login_required()
def moderate_publishing(id,idc):
    pub = db.session.query(Publishing).filter(Publishing.post_id==id,Publishing.channel_id==idc).first()
    print(pub)
    if request.method=="GET":
        return render_template('moderate_post.html', pub=pub)
    else:
        pub.title = request.form.get('titlepost')
        pub.description = request.form.get('descrpost')
        pub.link_url = request.form.get('linkurlpost')
        pub.image_url = request.form.get('imagepost')
        pub.date_from = datetime_converter(request.form.get('datefrompost'))
        pub.date_until = datetime_converter(request.form.get('dateuntilpost'))
        pub.state = 2
        return redirect(url_for('index'))

