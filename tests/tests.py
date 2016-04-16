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
from models import Trip
from main import setupWSGI


class BaseTestbedTest(unittest.TestCase):
    def setUp(self):
        # Then activate the testbed, which prepares the service stubs for use.
        self.testbed.activate()
        # Next, declare which service stubs you want to use.
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        # Clear ndb's in-context cache between tests.
        # This prevents data from leaking between tests.
        # Alternatively, you could disable caching by
        # using ndb.get_context().set_cache_policy(False)
        ndb.get_context().clear_cache()

    def tearDown(self):
        self.testbed.deactivate()


class BaseWebtestTest(unittest.TestCase):
    def setUp(self):
        self.testapp = webtest.TestApp("http://localhost:10080")  # I can't figure out how to set the port for webtest-ing a WSGIApplication
        # First, create an instance of the Testbed class.
        self.testbed = testbed.Testbed()


class ModelTests(BaseTestbedTest):
    pass


class RestTripTest(BaseWebtestTest):
    def setUp(self):
        super(RestTripTest, self).setUp()
        self.testapp.app.uri += "/api/v1"

    def test_get_trip(self):
        response = self.testapp.get('/trip')
        self.assertEqual(response.status_code, 200)
        assert 'application/json' in response.content_type
        assert 'My Trip' in response.json["results"][0]["name"]

    def test_post_trip(self):
        response = self.testapp.post('/trip', json.dumps({"name": "My Trip"}))
        postedTripID = response.json[0]["id"]
        response = self.testapp.get('/trip/' + postedTripID)
        self.assertEqual(response.status_code, 200)
        assert "My Trip" in response.json["name"]
        print self.testapp.app.uri

    def test_getting_non_existent_trip(self):
        with self.assertRaises(webtest.AppError):
            response = self.testapp.get('/trip/55f0cbb4236f44b7f0e3cb23')
            self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
