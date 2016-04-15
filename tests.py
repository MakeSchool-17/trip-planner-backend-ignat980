import server
import unittest
import json

from google.appengine.api import memcache
from google.appengine.ext import ndb
from google.appengine.ext import testbed
from models import Trip


class BaseApiTestCase(unittest.TestCase):
    def setUp(self):
        # First, create an instance of the Testbed class.
        self.testbed = testbed.Testbed()
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


class ModelTestCase(BaseApiTestCase):
    def test_posting_myobject(self):
        response = self.app.post('/trip/', data=json.dumps(Trip(name="My Trip")), content_type='application/json')

        responseJSON = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        assert 'application/json' in response.content_type
        assert 'My Trip' in responseJSON["name"]

    def test_getting_object(self):
        response = self.app.post('/trip/', data=json.dumps(dict(name="Another Trip")), content_type='application/json')

        postResponseJSON = json.loads(response.data.decode())
        postedObjectID = postResponseJSON["id"]

        response = self.app.get('/trip/' + postedObjectID)
        responseJSON = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        assert 'Another Trip' in responseJSON["name"]

    def test_getting_non_existent_object(self):
        response = self.app.get('/trip/55f0cbb4236f44b7f0e3cb23')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
