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
    if(size=="A5"):
        realSize=(420.94, 595.27)
    elif(size=="A4"):
        realSize=(595.27, 841.89)
    elif(size=="A3"):
        realSize=(841.27, 1190.54)

    # pdf = canvas.Canvas(titre + ".pdf", realSize)
    #
    # write_logo(pdf,image, realSize)
    # write_title(pdf, titre, realSize)
    # write_body(pdf,corps,realSize)
    # pdf.save()
    titre.replace(" ","_")
    outfilename = titre+".pdf"
    PDF_DIR = request.url_root + "static/pdf/"
    print(PDF_DIR)
    outfilepath = os.path.join(PDF_DIR, outfilename)
    doc = SimpleDocTemplate(outfilename, pagesize=letter,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=18)

    Story = []

    #Adding logo
    print("image path=",image)
    print(os.curdir)
    # /home/marc-henry/PycharmProjects/LINGI2255-2018-Superform-MS-06/superform/superform/plugins/logos/UCL.png

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


def write_logo(canvas, image, realSize):
    leftMarge = realSize[1]*0.4
    topMarge = realSize[1]*0.85
    #imagePath = request.url_root + "superform/plugins/logos/"+image+".png"
    imagePath = image+".png"
    canvas.drawImage(imagePath, leftMarge,topMarge )



def write_title(canvas, titre, realSize):

    myTitle = canvas.beginText()
    myTitle.setCharSpace(3)
    leftMarge = realSize[1]*0.1
    topMarge = realSize[1]*0.9
    myTitle.setTextOrigin(leftMarge,topMarge)
    myTitle.textLine(titre)
    canvas.drawText(myTitle)


def write_body(canvas, body, realSize):

    canvas.setFont("Times-Roman", 10*realSize[1]/800)
    myText = canvas.beginText()
    myText.setCharSpace(3)
    leftMarge = realSize[0]*0.1
    topMarge = realSize[1]*0.8
    myText.setTextOrigin(leftMarge,topMarge)
    words = body.split()
    n = 9  # number of words per line
    lignes = [' '.join(words[i:i + n]) for i in range(0, len(words), n)]

    for i in range(0, len(lignes) - 1):
        myText.textLine(lignes[i])
    canvas.drawText(myText)

