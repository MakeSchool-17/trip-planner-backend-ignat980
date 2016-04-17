# https://github.com/HunterLarco/Trip-Planner-Live-Coding-Backend/blob/master/models.py
# Hunter guided me through the process of making these models, and that the server
# does not directly talk to the mongo db, but it sends commands to the models that then talk to the db
# ENCRYPTION IMPORTS
# import bcrypt
from google.appengine.ext import ndb
from rest_gae.users import User


class Trip(ndb.Model):
    name = ndb.StringProperty()
    owner = ndb.KeyProperty(kind=User)
    date = ndb.DateTimeProperty(auto_now_add=True)

    def get_by_url(self, trip_id):
        trip_key = ndb.Key(urlsafe=trip_id)
        return trip_key.get()

    class RESTMeta:
        user_owner_property = 'owner'


class Waypoint(ndb.Model):
    name = ndb.StringProperty()
    location = ndb.GeoPtProperty(required=True)
    trip = ndb.KeyProperty(kind=Trip)

# class User(DBModel):
#     """
#     ' Extension of DBModel to implement user data-storage.
#     """
#
#     """ CLASS CONSTANTS """
#     BCRYPT_ROUNDS = 12
#
#     def __init__(self, username=None, *args, **kwargs):
#         """
#         ' Initializes the current model using DBModel's inherited
#         '   __init__ function with the added ability to initialize based
#         '   on username.
#         ' PARAMETERS
#         '   *args
#         '   <str username>
#         '   **kwargs
#         ' RETURNS
#         '   <User extends DBModel user_model>
#         """
#         super(User, self).__init__(*args, **kwargs)
#         if username:
#             self._queryload({'username': username})
#
#     def set_password(self, password):
#         """
#         ' Ecnrypts and sets the provided password
#         ' PARAMETERS
#         '   <str password>
#         ' RETURNS
#         '   None
#         ' NOTES
#         '   1. Uses bcrypt library
#         """
#         encodedpassword = password.encode('utf-8')
#         hashed = bcrypt.hashpw(encodedpassword, bcrypt.gensalt(self.BCRYPT_ROUNDS))
#         self.set('password', hashed)
#
#     def compare_password(self, password):
#         """
#         ' Given a password, compare it to the saved password.
#         ' PARAMETERS
#         '   <str password>
#         ' RETURNS
#         '   <bool is_same> True if passwords match, False if not.
#         """
#         encodedpassword = password.encode('utf-8')
#         return bcrypt.hashpw(encodedpassword, self.get('password')) == self.get('password')
#
#     def save(self):
#         """
#         ' Saves the current model using DBModel's inherited save method
#         '   with the added functionality of rejecting a username that already
#         '   exists in the database if this model has not been loaded from an
#         '   existing document.
#         ' PARAMETERS
#         '   None
#         ' RETURNS
#         '   <bool success> True if saved, False if not.
#         """
#         if not self.is_saved:
#             query = self.fetch({'username': self.get('username')})
#             if len(query) > 0:
#                 return False
#         return super(User, self).save()
