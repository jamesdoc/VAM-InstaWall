#!/usr/bin/env python

from google.appengine.ext import db

class DictModel(db.Model):
    def to_dict(self):
       return dict([(p, unicode(getattr(self, p))) for p in self.properties()])

class InstaStore(DictModel):
    caption = db.TextProperty()
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


