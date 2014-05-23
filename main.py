#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import webapp2
import config
import urllib2
import json
#import pprint
import datetime

from google.appengine.ext import db

API_ENDPOINT = 'https://api.instagram.com/v1/'


class InstaStore(db.Model):
    caption = db.StringProperty()
    created = db.DateTimeProperty()
    image_id = db.Key()
    image_photo_url = db.LinkProperty()
    image_photo_thumbnail_url = db.LinkProperty()
    image_url = db.LinkProperty()
    user_avatar_url = db.StringProperty()
    user_id = db.StringProperty()
    user_name = db.StringProperty()
    user_real_name = db.StringProperty()
    user_url = db.StringProperty()


class MainHandler(webapp2.RequestHandler):
    def get(self):

        #pp = pprint.PrettyPrinter(indent=4)

        url = 'https://api.instagram.com/v1/locations/' + config.location_id + '/media/recent?client_id=' + config.client_id

        req = urllib2.Request(url)
        res = urllib2.urlopen(req)

        jsn = json.loads(res.read())
        jsn = jsn['data']

        for image in jsn:

            try:
                caption = image['caption']['text']
            except TypeError:
                caption = ''

            insta_img = InstaStore(
                caption=caption,
                created=datetime.datetime.fromtimestamp(int(image['created_time'])),
                image_id=image['id'],
                image_photo_url=image['images']['standard_resolution']['url'],
                image_photo_thumbnail_url=image['images']['thumbnail']['url'],
                image_url=image['link'],
                user_avatar_url=image['user']['profile_picture'],
                user_id=image['user']['id'],
                user_name=image['user']['username'],
                user_real_name=image['user']['full_name'],
                user_url='http://instagram.com/%s' % image['user']['username']
            )
            insta_img.put()


            self.response.write('<div style="display: block;">')
            self.response.write('<img src="' + image['images']['standard_resolution']['url'] + '"/><br />')
            self.response.write('User: ' + image['user']['full_name'] + '<br />')

            try:
                self.response.write('Text: ' + image['caption']['text'] + '<br />')
            except TypeError:
                continue

            self.response.write(image)
            self.response.write('</div>')
            #pp.pprint(image)


app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
