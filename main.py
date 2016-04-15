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
import webapp2
import os
import sys

REST_GAE_PROJECT_DIR = os.path.join(os.path.dirname(__file__), 'vendor/rest_gae')
sys.path.append(REST_GAE_PROJECT_DIR)

from models import Trip, Waypoint
from rest_gae import *
from rest_gae.users import UserRESTHandler


class MainHandler(webapp2.RequestHandler):
    def get(self, trip_id):
        trip = Trip.get_by_url(trip_id)
        print trip
        if trip is None:
            self.error(404)
        else:
            self.response.out.write(trip)

    def post(self):
        name = self.request.get("name")
        trip = Trip(name=name, waypoints=None)
        trip_key = trip.put()
        trip_url = '/trip/' + trip_key.urlsafe()
        print trip_url
        self.redirect(trip_url)
        self.response.out.write("Trip:" + trip + "; trip_key = " + trip_key + "; trip_url = " + trip_url)
        # Redirect to trip?

config = {
    'webapp2_extras.sessions': {
        'secret_key': 'my-super-secret-key',
    }
}

app = webapp2.WSGIApplication([
    RESTHandler(
        '/api/v1/trip',
        Trip,
        permissions={
            'GET': PERMISSION_ANYONE,
            'POST': PERMISSION_LOGGED_IN_USER,
            'PUT': PERMISSION_OWNER_USER,
            'DELETE': PERMISSION_OWNER_USER
        },

    ),
    # (r'/(.*)?', MainHandler),
], config=config, debug=True)
