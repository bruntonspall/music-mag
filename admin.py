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

import logging

class AdminHandler(webapp.RequestHandler):
    def get(self):
        value = KVStore.all().filter('name =', 'CurrentEdition').get()
        if value:
            self.redirect('/admin/%d' % value.value)
        else:
            current_edition = KVStore(name='CurrentEdition')
            current_edition.value = 1
            current_edition.save()
            self.redirect('/admin/1')

class AdminEditionHandler(webapp.RequestHandler):
    def get(self, edition):
        render_admin_template(self, 'admin.html', {'pages':Page.all().order('number'), 'edition': edition})
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

class PopulateHandler(webapp.RequestHandler):
    def get(self):
        #Get Guardian Music Tags
        content = json.loads(urlfetch.fetch(GUARDIAN_API_HOST+"/tags.json?section=music").content)
        total = content['response']['pages']
        for page in range(total):
            taskqueue.add(url='/admin/populate/worker', params={'page':page+1}, method='POST')
        self.response.out.write('OK')

class PopulateWorkerHandler(webapp.RequestHandler):
    def post(self):
        url = GUARDIAN_API_HOST+"/tags.json?section=music&page=%s" % (self.request.get('page'))
        logging.info('requesting %s', url)
        content = json.loads(urlfetch.fetch(url).content)
        for tag in content['response']['results']:
            obj = Tag.all().filter('name =',tag['webTitle']).get()
            if obj:
                obj.name = tag['webTitle']
                obj.guardian_id = tag['id']
                obj.save()
            else:
                Tag(name=tag['webTitle'],guardian_id=tag['id'], lastfm_id=tag['id']).save()
        self.response.out.write('OK')

def main():
    application = webapp.WSGIApplication([
        ('/admin', AdminHandler),
        ('/admin/(?P<edition>\d+)', AdminEditionHandler),
        ('/admin/populate', PopulateHandler),
        ('/admin/populate/worker', PopulateWorkerHandler),
    ],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
