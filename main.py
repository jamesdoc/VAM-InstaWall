#!/usr/bin/env python

from model import InstaStore
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
        return q.get()

    def get(self):
        image = self.get_latest_image()
        self.response.write("<img src='%s' alt='' />" % image.image_photo_url)


app = webapp2.WSGIApplication([
    ('/import/(.*)', importer.ImportHandler),
    ('/', MainHandler)
], debug=True)
