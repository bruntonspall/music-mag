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
from models import *


class MainHandler(webapp.RequestHandler):
    def get(self):
        value = KVStore.all().filter('name =', 'CurrentEdition').get()
        if value:
            self.redirect('/edition/%d' % value.value)
        render_template(self, 'noedition.html', {})

class EditionHandler(webapp.RequestHandler):
    def get(self, edition):
        render_template(self, 'edition.html', {'pages': Page.all().filter('edition =', int(edition)).order('number')})

class TagsHandler(webapp.RequestHandler):
    def get(self):
        term = self.request.get('term')
        tags = Tag.all()
        if term:
            tags.filter('name >',term).filter('name < ',term+u'\ufffd')
        render_template(self, 'tags.json', {'tags': tags, 'callback':self.request.get('callback')})
        
class ContentHandler(webapp.RequestHandler):
    def get(self, tag):
        render_template(self, 'content.json', {'tag': Tag.all().filter('guardian_id =',tag).get(), 'callback':self.request.get('callback')})

def main():
    application = webapp.WSGIApplication([
        ('/', MainHandler),
        ('/edition/(?P<edition>\d+)', EditionHandler),
        ('/api/tags.json', TagsHandler),
        ('/api/tag/(?P<tag>[a-z/-]+).json', ContentHandler),
    ],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
