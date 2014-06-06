#!/usr/bin/env python

import jinja2
import os
import webapp2
from api import GetImages
from datetime import datetime, timedelta
from importer import ImportHandler, TruncateData
from shop_wall.importer import ShopImportHandler

from settings import JINJA_ENVIRONMENT

from shop_wall.shopwall_handler import ShopWallHandler

class MainHandler(webapp2.RequestHandler):

    def get(self):
        one_day_ago = datetime.today() - timedelta(1)
        data = {
            'image':  GetImages().select_by_date(one_day_ago, '<='),
            'dt': one_day_ago
            }
        template = JINJA_ENVIRONMENT.get_template('template/instagram.html')
        self.response.write(template.render(data))


app = webapp2.WSGIApplication([
    ('/api/v1/get_images.json', GetImages),
    ('/import/(.*)', ImportHandler),
    ('/truncate', TruncateData),
    ('/shop', ShopWallHandler),
    ('/shop/', ShopWallHandler),
    # ('/shopimporter', ShopImportHandler),
    ('/', MainHandler)
], debug=True)
