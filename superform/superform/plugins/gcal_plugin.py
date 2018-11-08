from flask import current_app, session, flash
from superform.models import db, User 
import json


FIELDS_UNAVAILABLE = ['Image']