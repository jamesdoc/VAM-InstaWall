#!/usr/bin/env python

import jinja2
import os
import webapp2
from api import GetImages
from datetime import datetime, timedelta
<<<<<<< HEAD
from importer import ImportHandler
=======
from importer import ImportHandler, TruncateData
from shop_wall.importer import ShopImportHandler
>>>>>>> 03a5b7bb0e33116f8a83c091f10361eb5f197178

from settings import JINJA_ENVIRONMENT

from shop_wall.shopwall_handler import ShopWallHandler
from whats_on.whats_on_handler import WhatsOnHandler

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
    ('/shop', ShopWallHandler),
    ('/whatson', WhatsOnHandler),
    ('/', MainHandler)
], debug=True)
