#!/usr/bin/env python

from model import InstaStore

import config
import datetime
import json
import random
import urllib2
import webapp2

API_ENDPOINT = 'https://api.instagram.com/v1/'
MAX_IMPORT = 30

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
            url = '%stags/%s/media/recent?client_id=%s' % (API_ENDPOINT, random.choice(config.tags), config.client_id)
        #elif filter == 'user':
        #   url = 'https://api.instagram.com/v1/users/' + config.user_id + '/media/recent?client_id=' + config.client_id
        else:
            url = '%slocations/%s/media/recent?client_id=%s' % (API_ENDPOINT, config.location_id, config.client_id)

        print url

        while i < MAX_IMPORT:

            response = self.get_url_contents(url)

            jason = json.loads(response.read())
            images = jason['data']
            flag = False

            for image in images:
                print image['id']

                if self.does_image_id_exist(image['id']):
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