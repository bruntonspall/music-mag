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
#
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from helpers import *
from google.appengine.ext.webapp.util import login_required

class MainHandler(webapp.RequestHandler):
    def get(self):
        render_template(self, 'home.html', {'message':'World'})

class AdminHandler(webapp.RequestHandler):
    @login_required
    def get(self):
        render_admin_template(self, 'home.html', {})

class EditionHandler(webapp.RequestHandler):
    def get(self, edition=None):
        render_template(self, 'issue.html', {'edition': edition})



def main():
    application = webapp.WSGIApplication([('/', MainHandler),
    ('/admin', AdminHandler),
    ('/issue(?:/(?P<edition>\d+))?', EditionHandler)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
