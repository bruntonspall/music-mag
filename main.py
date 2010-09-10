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
from google.appengine.ext.webapp.util import login_required

from helpers import *
from models import *

import logging

class AdminHandler(webapp.RequestHandler):
    @login_required
    def get(self):
        value = KVStore.all().filter('name =', 'CurrentEdition').get()
        if value:
            self.redirect('/admin/%d' % value)
        else:
            current_edition = KVStore(name='CurrentEdition')
            current_edition.value = 1
            current_edition.save()
            self.redirect('/admin/1')

class AdminEditionHandler(webapp.RequestHandler):
    @login_required
    def get(self, edition):
        render_admin_template(self, 'admin.html', {'pages':Page.all().order('number'), 'edition': edition})

            
class MainHandler(webapp.RequestHandler):
    def get(self):
        value = KVStore.all().filter('name =', 'CurrentEdition').get()
        if value:
            self.redirect('/edition/%d' % value.value)
        render_template(self, 'noedition.html', {})

class EditionHandler(webapp.RequestHandler):
    def get(self, edition):
        render_template(self, 'edition.html', {'pages': Page.all().filter('edition =', int(edition)).order('number')})

    def post(self, edition):
        logging.info('Posting to edition')
        for i,arg in enumerate(self.request.arguments()):
            logging.info('Item %d is %s', i, arg)
            id = arg.strip("[]")
            content = get_content_for_guardian_id(id)
            logging.info("Got content for %s - '%s' - image: %s", id, content['headline'], content['image'])
            obj = Page.all().filter('number =',i+1).filter('edition =', edition).get()
            if obj:
                obj.guardian_article_id=id
                obj.headline=content['headline']
                obj.trailtext=content['trailtext']
                obj.body=content['body']
                obj.image=content['image']
                obj.save()
            else:
                Page(number=i+1, guardian_article_id=id, headline=content['headline'], trailtext=content['trailtext'], body=content['body'], image=content['image'], edition=int(edition)).save()

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

class PopulateHandler(webapp.RequestHandler):
    @login_required
    def get(self):
        Tag.populate()
        self.response.out.write('OK')

def main():
    application = webapp.WSGIApplication([
        ('/', MainHandler),
        ('/admin', AdminHandler),
        ('/admin/(?P<edition>\d+)', AdminEditionHandler),
        ('/admin/populate', PopulateHandler),
        ('/edition/(?P<edition>\d+)', EditionHandler),
        ('/api/tags.json', TagsHandler),
        ('/api/tag/(?P<tag>[a-z/-]+).json', ContentHandler),
    ],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
