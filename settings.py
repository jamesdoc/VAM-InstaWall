
import jinja2
import os
import webapp2
from api import GetImages
from datetime import datetime, timedelta
from importer import ImportHandler, TruncateData



JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)