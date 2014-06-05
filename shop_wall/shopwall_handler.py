#!/usr/bin/env python

import jinja2
import os
import webapp2
from main import JINJA_ENVIRONMENT
class ShopWallHandler(webapp2.RequestHandler):
    def get(self):
        data = {
            'image':  [1,2,3,4],
            'dt': 3
            }
        template = JINJA_ENVIRONMENT.get_template('template/shopwall.html')
        self.response.write(template.render(data))


