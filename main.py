#!/usr/bin/env python

from api import GetImages
from datetime import datetime, timedelta

from importer import ImportHandler, TruncateData
import jinja2
import os
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class MainHandler(webapp2.RequestHandler):

    def get(self):
        one_day_ago = datetime.today() - timedelta(1)
        data = {
            'image':  GetImages().select_by_date(one_day_ago, '<='),
            'dt': one_day_ago
            }
        template = JINJA_ENVIRONMENT.get_template('template/base.html')
        self.response.write(template.render(data))


app = webapp2.WSGIApplication([
    ('/api/v1/get_images.json', GetImages),
    ('/import/(.*)', ImportHandler),
    ('/truncate', TruncateData),
    ('/', MainHandler)
], debug=True)
