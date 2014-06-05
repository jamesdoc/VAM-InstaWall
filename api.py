#!/usr/bin/env python
from google.appengine.ext import db
from model import InstaStore
import webapp2
import json
import datetime

class GetImages(webapp2.RequestHandler):

    def select_by_date(self, dt, sign = '>'):
        return db.GqlQuery(
            "SELECT * FROM InstaStore WHERE created %s DATETIME(:1, :2, :3, :4, :5, :6) ORDER BY created DESC LIMIT 50"
                           %    sign,
                                int(dt.strftime('%Y')),
                                int(dt.strftime('%m')),
                                int(dt.strftime('%d')),
                                int(dt.strftime('%H')),
                                int(dt.strftime('%M')),
                                int(dt.strftime('%S'))
        )


    def get(self):
        instaImages = InstaStore.all()
        datestamp = self.request.get('dt', '')
        self.response.headers['Content-Type'] = 'application/json'
        self.response.headers.add_header("Access-Control-Allow-Origin", "*")
        try:
            datestamp = datetime.datetime.strptime(datestamp, '%Y%m%d%H%M%S')
            print datestamp
        except ValueError:
            self.response.write(json.dumps({'error': 'Unrecognised datetime, should be like '
                                                     '/api/v1/get_images.json?dt=20140101000000 '
                                                     'where dt=YYYYMMDDHHMMSS'}))
            return
        results = self.select_by_date(datestamp)
        self.response.write(json.dumps([t.to_dict() for t in results]))

