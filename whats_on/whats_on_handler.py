#!/usr/bin/env python

import json
import jinja2
import webapp2
from datetime import datetime
from main import JINJA_ENVIRONMENT
from importer import ImportHandler

WHATS_ON_API_URL = "http://www.vam.ac.uk/whatson/json/events/day/"
IGNORED_EVENT_TYPES = [2, 30, 31]
EVENT_TYPES = {
    2: 'Family Event',
    15: 'Workshop',
    24: 'Special Event',
    30: 'Exhibition',
    31: 'Display',
    39: 'Year Course',
    40: 'Evening Talk',
    41: 'Tour',
    44: 'Seminar',
    45: 'Members Event'
}

class WhatsOnHandler(webapp2.RequestHandler):

    def filter_events(self, events=None):
        if events is None:
            return

        event_list = {}
        for event in events:
            if event['fields']['event_type'] not in IGNORED_EVENT_TYPES:
                for date in event['extras']['today_slots'].split(','):
                    event_list[date] = event['fields']
        return event_list

    def get_events(self, day=None):

        if day is None:
            day = datetime.today()
            day = day.strftime("%Y%m%d")

        url = WHATS_ON_API_URL + day

        i = ImportHandler()
        data = i.get_url_contents(url)
        return json.loads(data.read())

    def get(self):

        events = self.get_events()
        events = self.filter_events(events)

        data = {
            'events': events,
            'event_types': EVENT_TYPES
        }
        template = JINJA_ENVIRONMENT.get_template('template/whatson.html')
        self.response.write(template.render(data))

