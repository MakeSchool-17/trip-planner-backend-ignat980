from models import *
from google.appengine.api import users


class Seeder(object):
    def seed(self):
        self.user1 = User(
            email=users.User('1@gmail.com')
        )
        self.user1.put()
        self.user2 = User(
            email=users.User('2@gmail.com')
        )
        self.user2.put()
        self.trip1 = Trip(
            name="Test trip",
            owner=self.user1.key
        )
        self.trip1.put()

    def clean(self):
        def __():
            for m in [User, Trip]:
                for e in m.query().fetch(1000):
                    yield e

        for k in __():
            k.key.delete()
