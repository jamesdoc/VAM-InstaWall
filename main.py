#!/usr/bin/env python

from google.appengine.ext import db

import config
import datetime
import jinja2
import json
import os
import urllib2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

API_ENDPOINT = 'https://api.instagram.com/v1/'
MAX_IMPORT = 20

class InstaStore(db.Model):
    caption = db.StringProperty(multiline=True)
    created = db.DateTimeProperty()
    image_id = db.StringProperty()
    image_photo_url = db.LinkProperty()
    image_photo_thumbnail_url = db.LinkProperty()
    image_url = db.LinkProperty()
    user_avatar_url = db.StringProperty()
    user_id = db.StringProperty()
    user_name = db.StringProperty()
    user_real_name = db.StringProperty()
    user_url = db.StringProperty()


class MainHandler(webapp2.RequestHandler):

    def get_latest_image(self):
        q = InstaStore.all()
        #q.filter('id =', '709967152837643989_390861362')
        q.order('-created')
        result = q.get()
        return result

    def get(self):
        image = self.get_latest_image()

        self.response.write("<img src='%s' alt='' />" % image.image_photo_url)


class ImportHandler(webapp2.RequestHandler):
    # Returns true if image exists
    def does_image_id_exist(self, image_id):
        q = InstaStore.all(keys_only=True)
        q.filter('image_id =', image_id)
        result = q.get()

        if result:
            return True

        return False

    # Gets the contents of a given url
    def get_url_contents(self, url):
        req = urllib2.Request(url)
        return urllib2.urlopen(req)

    # Adds one image into the datastore
    def insert_to_datastore(self, image):

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

        print 'Added %s to the datastore' % image['link']

    def get(self, filter):
        self.response.write('Importing...')
        i = 0

        if filter == 'tag':
            url = 'https://api.instagram.com/v1/tags/' + config.location_id + '/media/recent?client_id=' + config.client_id
        elif filter == 'user':
            url = 'https://api.instagram.com/v1/users/' + config.user_id + '/media/recent?client_id=' + config.client_id
        else:
            url = 'https://api.instagram.com/v1/locations/' + config.location_id + '/media/recent?client_id=' + config.client_id

        print url

        while i < MAX_IMPORT:

            response = self.get_url_contents(url)

            jason = json.loads(response.read())
            images = jason['data']
            flag = False

            for image in images:
                print image['id']

                if self.does_image_id_exist(image['id']) is True:
                    continue

                self.insert_to_datastore(image)
                flag = True

                self.response.write('<hr />')
                self.response.write('<div style="display: block;">')
                self.response.write('<a href="' + image['link'] + '" target="_blank"><img src="' + image['images']['thumbnail']['url'] + '"/></a><br />')
                self.response.write('</div>')

            if flag is False:
                i = MAX_IMPORT

            url = jason['pagination']['next_url']
            i += 1

app = webapp2.WSGIApplication([
    ('/import/(.*)', ImportHandler),
    ('/', MainHandler)
], debug=True)
