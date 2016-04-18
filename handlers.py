import webapp2
import json
from models import Trip, Waypoint
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


def after_put(created_keys, trip, json_data):
    print "Trip after post"
    print trip
    print "Keys"
    print created_keys
    print "Data"
    print json_data

    # Get all waypoints that belong to this trip
    query = Waypoint.query().filter(Waypoint.trip == trip[0].key)
    trip_waypoints = query.fetch(100)
    print 'Waypoints: {}'.format(trip_waypoints)
    new_waypoint = True
    # For each new waypoint either add it or update
    for waypoint in json_data[0]['waypoints']:
        # Find the json waypoint in the old waypoint
        for wp in trip_waypoints:
            not_found = True
            # Check for the waypoint in the json
            for p in json_data[0]['waypoints']:
                if wp.name == p['name']:
                    print 'The Waypoint %s is in the json' % (p['name'])
                    not_found = False
                    break
            # If the waypoint is not in the json, delete it
            if not_found:
                print 'Deleted a waypoint that is not in the json'
                wp.key.delete()
                trip_waypoints = query.fetch(100)
            # If the current json waypoint is in the old data, update it
            if waypoint['name'] == wp.name:
                print 'Updated a waypoint'
                wp.location = ndb.GeoPt(waypoint['lat'], waypoint['lon'])
                wp.put()
                new_waypoint = False
        if new_waypoint:
            print 'Added a new waypoint'
            w = Waypoint(
                name=waypoint['name'],
                location=ndb.GeoPt(waypoint['lat'], waypoint['lon']),
                trip=created_keys[0]
            )
            w.put()
    return trip


def after_get(trips):
    print 'After get'
    print trips
    if isinstance(trips, list):
        for trip in trips:
            query = Waypoint.query().filter(Waypoint.trip == trip.key)
            waypoints = query.fetch(100)
            trip.waypoints = [waypoint.to_dict() for waypoint in waypoints]
    else:
        query = Waypoint.query().filter(Waypoint.trip == trips.key)
        waypoints = query.fetch(100)
        trips.waypoints = [waypoint.to_dict() for waypoint in waypoints]
    return trips


def after_delete(keys, trips):
    for key in keys:
        query = Waypoint.query().filter(Waypoint.trip == key)
        waypoints = query.fetch(100)
        for waypoint in waypoints:
            waypoint.key.delete()
