#!/usr/bin/env python
from google.appengine.ext import db
from model import InstaStore
import webapp2
import json

class GetImages(webapp2.RequestHandler):

    def get(self):

        datestamp = self.request.get('dt', '')

        if datestamp is "":
            datestamp = 20140529

        q = InstaStore.all()
        #q.filter('created >', datestamp)
        q.order('-created')
        test = q.run(limit=50)

        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps([t.to_dict() for t in test]))


