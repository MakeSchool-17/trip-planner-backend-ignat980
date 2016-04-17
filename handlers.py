import webapp2
from models import Waypoint
from google.appengine.ext import ndb


class TripHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write("Hello")


def after_post(created_keys, trip, json_data):
    print "Trip after post"
    print trip
    print "Keys"
    print created_keys
    print "Data"
    print json_data

    for waypoint in json_data[0]['waypoints']:
        w = Waypoint(
            name=waypoint['name'],
            location=ndb.GeoPt(waypoint['lat'], waypoint['lon']),
            trip=created_keys[0]
        )
        w.put()
    return trip
