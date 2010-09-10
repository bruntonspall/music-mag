#!/usr/bin/env python
# encoding: utf-8
"""
models.py

Created by MBS on 2010-08-13.
Copyright (c) 2010 __MyCompanyName__. All rights reserved.
"""
from google.appengine.ext import db
from google.appengine.api import urlfetch

import logging
from google.appengine.api.labs import taskqueue

try:
    import json
except ImportError:
    from django.utils import simplejson as json

from settings import *

if IS_LOCAL_API:
    GUARDIAN_API_HOST = 'http://localhost:8700/content-api/api'
else:
    GUARDIAN_API_HOST = 'http://content.guardianapis.com'

class Tag(db.Model):
    name = db.StringProperty(required=True)
    guardian_id = db.StringProperty(required=True)
    lastfm_id = db.StringProperty(required=True)
    
    @staticmethod
    def populate():
        #Get Guardian Music Tags
        page = 1
        total = 51
        content = json.loads(urlfetch.fetch(GUARDIAN_API_HOST+"/tags.json?section=music").content)
        total = content['response']['pages']
        for page in range(total):
            taskqueue.add(url='/admin/populate/worker', params={'page':page+1}, method='POST')

    @staticmethod
    def populate_page(page):
        url = GUARDIAN_API_HOST+"/tags.json?section=music&page=%s" % (page)
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


    def get_guardian_articles(self):
        url = GUARDIAN_API_HOST+"/%s.json?show-fields=all&api-key=%s" % (self.guardian_id, GU_API_KEY)
        logging.info("Requesting %s", url)
        response = json.loads(urlfetch.fetch(url).content)
        return [{'headline':content["fields"]["headline"], 
                 'trailtext':content["fields"]["trailText"],
                 'id':content["id"]} for content in response["response"]["results"]]
        
class Page(db.Model):
    edition = db.IntegerProperty(required=True)
    number = db.IntegerProperty(required=True)
    guardian_article_id = db.StringProperty(required=False)
    headline = db.StringProperty(required=True)
    trailtext = db.StringProperty(required=True)
    body = db.TextProperty(required=True)
    image = db.StringProperty(required=False)
    
def get_content_for_guardian_id(id):
    url = GUARDIAN_API_HOST+"/%s.json?show-fields=all&api-key=%s" % (id, GU_API_KEY)
    if IS_PARTNER:
        url += "&show-media=picture"
    if IS_LOCAL_API:
        if IS_PARTNER:
            url += "&userTier=partner"
        else:
            url += "&userTier=approved"
            
    logging.info("Requesting %s", url)
    response = json.loads(urlfetch.fetch(url).content)
    content = response["response"]["content"]
    image = None
    if content.has_key('mediaAssets'):
        image = content["mediaAssets"][0]["file"]
    return {'headline':content["fields"]["headline"], 'trailtext':content["fields"]["trailText"],'body':content["fields"]["body"], 'image':image,'id':content["id"]}


class KVStore(db.Expando):
    name = db.StringProperty(required=True)