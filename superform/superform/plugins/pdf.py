"""
author: Team 06
date: December 2018
Plugin for the PDF feature
"""

import json

from flask import url_for, redirect
from reportlab.pdfgen import canvas
import json
from flask import current_app, request
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph
from pathlib import Path
import os
import time

FIELDS_UNAVAILABLE = []

CONFIG_FIELDS = ["Format", "Logo"]


def run(publishing, channel_config):
    """ Gathers the informations in the config column and launches the
    posting process
    channel_config format = {image : ??, size : "A4"}"""
    # TODO
    json_data = json.loads(channel_config)
    title = publishing.title
    body = publishing.description
    image = json_data['Logo']
    size = json_data['Format']
    datas = create_pdf(title, body, image, size)

    path = datas[0]
    outputFile = datas[1]
    import webbrowser
    webbrowser.open_new_tab('file://' + path)

    #data_folder = Path("superform/plugins/pdf")
    #file_to_delete = data_folder / outputFile
    #file_to_delete = "DELETEMEPLEASE.txt"
    #time.sleep(1)
    #os.remove(file_to_delete)


def export(post_id, idc):
    """
    Launches the export process
    :return:
    """
    print("Here is the export method")
    print('post_id = %s\nchan_id = %s' % (post_id, idc))

    # TODO get the post information
    # db.session... TODO
    # pub = {'description': post.description, 'title': post.title} TODO
    # config = TODO
    # run(publishing = pub, channel_config = config)
    return redirect(url_for('index'))


def create_pdf(titre, corps, image, size):

    empryString = ""
    fileTitle = empryString.join(e for e in titre if e.isalnum())
    if(len(fileTitle))==0:
        fileTitle="DEFAULT"
    outfilename = fileTitle+".pdf"
    localPath = os.path.dirname(__file__)+"/pdf/"+outfilename

    doc = SimpleDocTemplate(localPath, pagesize=letter,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=18)

    Story = []

    #Adding logo
    print("image path=",image)
    print(os.curdir)


    im = Image(image+".png")  # , 2 * inch, 2 * inch)
    Story.append(im)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY, leading=15))
    Story.append(Spacer(1, 20))

    #Adding title
    p_font = 24
    Story.append(Spacer(1, 30))
    # ptext = '<font name=HELVETICA>'+title+'</font>' % p_font
    rr = """<font name=times-roman size=%s>{}</font>
        """.format(titre) % p_font
    Story.append(Paragraph(rr, styles["Normal"]))
    Story.append(Spacer(6, 26))

    #Adding body
    p_font = 13
    text = """<font name=times-roman size=%s>{}</font>
        """.format(corps) % p_font
    Story.append(Paragraph(text, styles["Justify"]))
    Story.append(Spacer(6, 12))

    #Saving pdf
    doc.build(Story)
    datas = [localPath, outfilename]
    return datas