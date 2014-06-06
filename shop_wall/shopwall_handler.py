#!/usr/bin/env python

import jinja2
import json
from google.appengine.api import urlfetch

import os
import webapp2
from settings import JINJA_ENVIRONMENT


class ShopWallHandler(webapp2.RequestHandler):
    def get(self):
        q = self.request.get('q',default_value='italian')
        url = "http://www.vam.ac.uk/api/v2/shop-index/shop-item/?q=%s" % q
        result = urlfetch.fetch(url)
        if result.status_code == 200:
            p =  json.loads(result.content)
            data = {
                'image':  p['data'],
                }
            template = JINJA_ENVIRONMENT.get_template('template/shopwall.html')
            self.response.write(template.render(data))

