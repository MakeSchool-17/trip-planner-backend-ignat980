import os
import sys

sys.path.insert(0, '/usr/local/google_appengine/python')
import dev_appserver
dev_appserver.fix_sys_path()

import webtest
import webapp2
import unittest
import json

from google.appengine.api import memcache
from google.appengine.ext import ndb
from google.appengine.ext import testbed
from models import MyUser, Trip, Waypoint
from main import setupWSGI
from seeds import Seeder


class BaseTestbedTest(unittest.TestCase):
    def setUp(self):
        # First, create an instance of the Testbed class.
        self.testbed = testbed.Testbed()
        # Then activate the testbed, which prepares the service stubs for use.
        self.testbed.activate()
        # Next, declare which service stubs you want to use.
        self.testbed.init_datastore_v3_stub("/tmp/trip-planner-datastore")
        self.testbed.init_memcache_stub()
        # Clear ndb's in-context cache between tests.
        # This prevents data from leaking between tests.
        # Alternatively, you could disable caching by
        # using ndb.get_context().set_cache_policy(False)
        ndb.get_context().clear_cache()

    def tearDown(self):
        self.testbed.deactivate()


class BaseWebtestTest(unittest.TestCase, Seeder):
    def setUp(self):
        # Create an instance of webtest
        self.testapp = webtest.TestApp("http://localhost:8080")  # I can't figure out how to set the port for webtest-ing a WSGIApplication
        # Create an instance of the Testbed class.
        self.testbed = testbed.Testbed()
        # Then activate the testbed, which prepares the service stubs for use.
        self.testbed.activate()
        # Next, declare which service stubs you want to use.
        self.testbed.init_datastore_v3_stub(datastore_file="/tmp/trip-planner-datastore", use_sqlite=False, save_changes=True)
        self.testbed.init_memcache_stub()
        # Clear ndb's in-context cache between tests.
        # This prevents data from leaking between tests.
        # Alternatively, you could disable caching by
        # using ndb.get_context().set_cache_policy(False)
        ndb.get_context().clear_cache()
        self.seed()
        print User.query().fetch(5)
        # assert len(User.query().fetch(5)) == 2
        # assert len(Trip.query().fetch(5)) == 1

    def tearDown(self):
        self.testbed.deactivate()


class ModelTests(BaseTestbedTest):
    pass


class RestTripTest(BaseWebtestTest):
    def setUp(self):
        super(RestTripTest, self).setUp()
        self.testapp.app.uri += "/api/v1"

    def test_get_trip(self):
        response = self.testapp.get('/trip')
        self.assertEqual(response.status_code, 200, "Get at /trip should return 200 response")
        assert 'application/json' in response.content_type
        print response.json["results"]
        self.assertEqual(1, len(response.json["results"]), msg="Database should return initial Trip")
        self.assertEqual('Test trip', response.json["results"][0]["name"])

    def test_post_trip(self):
        response = self.testapp.post('/trip', json.dumps({"name": "My Trip"}))
        postedTripID = response.json[0]["id"]
        response = self.testapp.get('/trip/' + postedTripID)
        self.assertEqual(response.status_code, 200)
        self.assertEqual("My Trip", response.json["name"])

    def test_getting_non_existent_trip(self):
        with self.assertRaises(webtest.AppError):
            response = self.testapp.get('/trip/55f0cbb4236f44b7f0e3cb23')
            self.assertEqual(response.status_code, 404)

    def test_delete_trip(self):
        count = Trip.query(Trip.name == "My Trip").count(1)
        item = Trip.query(Trip.name == "My Trip").fetch(1)
        response = self.testapp.delete("/trip", json.dumps({"id": item[0].id}))
        self.assertEqual(201, response.status_code, "Delete at /trip/{id} should remove trip")
        self.assertEqual(count - 1, Trip.query(Trip.name == "My Trip").count(100), "Delete at /trip/{id} should have removed one item")


if __name__ == '__main__':
    unittest.main()
