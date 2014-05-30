#!/usr/bin/env python

from model import InstaStore

import api
import importer
import jinja2
import os
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainHandler(webapp2.RequestHandler):

    def get_latest_image(self):
        q = InstaStore.all()
        q.order('-created')
        return q.run(limit=50)

    def get(self):
        data = {}
        data['image'] = self.get_latest_image()

        template = JINJA_ENVIRONMENT.get_template('template/base.html')
        self.response.write(template.render(data))


app = webapp2.WSGIApplication([
    ('/api/v1/get_images.json', api.GetImages),
    ('/import/(.*)', importer.ImportHandler),
    ('/truncate', importer.TruncateData),
    ('/', MainHandler)
], debug=True)
