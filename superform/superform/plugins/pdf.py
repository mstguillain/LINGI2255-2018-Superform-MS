"""
author: Team 06
date: December 2018
Plugin for the PDF feature
"""

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
import os

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
    image = json_data['Logo'] # HOW WILL THE IMAGE BE STORED IN THE DB ?
    size = json_data['Format']
    create_pdf(title, body, image, size)


def export():
    """
    Launches the export
    :return:
    """
    print("Here is the export method")
    # TODO
    # run(publishing = None, channel_config = None)
    return redirect(url_for('index'))


def create_pdf(titre, corps, image, size):
    fileTitle = titre.replaceAll("[ -+.^:,']", "")
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
