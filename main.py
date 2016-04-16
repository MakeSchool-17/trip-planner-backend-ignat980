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


def userPolicy(user, data):
    if (len(data['password']) < 8):
        raise ValueError('Password too short')


def setupWSGI():
    config = {
        'webapp2_extras.sessions': {
            'secret_key': 'my-super-secret-key',
        }
    }

    return webapp2.WSGIApplication([
        RESTHandler(
            '/api/v1/trip',
            Trip,
            permissions={
                'GET': PERMISSION_ANYONE,
                'POST': PERMISSION_ANYONE,
                'PUT': PERMISSION_ANYONE,
                'DELETE': PERMISSION_ANYONE
            },

        ),

        UserRESTHandler(
            '/api/v1/users',  # The base URL for the user management endpoints
            # user_model='models.User',  # Use our own custom User class
            email_as_username=True,
            admin_only_user_registration=True,
            user_details_permission=PERMISSION_LOGGED_IN_USER,
            verify_email_address=True,
            verification_email={
                'sender': 'Ignat Remizov <ignat980@gmail.com>',
                'subject': 'Verify your email',
                'body_text': 'Hello {{ user.full_name }}, click here: {{ verification_url }}',
                'body_html': 'Hello {{ user.full_name }}, click <a href="{{ verification_url }}">here</a>'
            },
            verification_successful_url='/verified-user',
            verification_failed_url='/verification-failed',
            reset_password_url='/reset-password',
            reset_password_email={
                'sender': 'Ignat Remizov <ignat980@gmail.com>',
                'subject': 'Reset your password',
                'body_text': 'Hello {{ user.name }}, click here: {{ verification_url }}',
                'body_html': 'Hello {{ user.name }}, click <a href="{{ verification_url }}">here</a>'
            },
            send_email_callback=None,  # my_senc_func(email)
            allow_login_for_non_verified_email=False,
            user_policy_callback=userPolicy
        )
        # (r'/(.*)?', MainHandler),
    ], config=config, debug=True)

app = setupWSGI()
