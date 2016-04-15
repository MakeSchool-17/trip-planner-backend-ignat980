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


class MainHandler(webapp2.RequestHandler):
    def get(self, myobject_id):
        myobject_collection = app.db.myobjects
        myobject = myobject_collection.find_one({"_id": ObjectId(myobject_id)})

        if myobject is None:
            response = jsonify(data=[])
            response.status_code = 404
            return response
        else:
            return myobject
        print 'test'

    def post(self):
        new_myobject = request.json
        myobject_collection = app.db.myobjects
        result = myobject_collection.insert_one(new_myobject)

        myobject = myobject_collection.find_one({"_id": ObjectId(result.inserted_id)})

        return myobject

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
