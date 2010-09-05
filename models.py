#!/usr/bin/env python
# encoding: utf-8
"""
models.py

Created by MBS on 2010-08-13.
Copyright (c) 2010 __MyCompanyName__. All rights reserved.
"""
from google.appengine.api import memcache
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from google.appengine.ext.db import djangoforms
from google.appengine.api import urlfetch


import random
import datetime
import time
import logging
import json

import helpers
from settings import *

#GUARDIAN_API_HOST = 'http://localhost:8700/content-api/api'
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
        while (page <= total):
            url = GUARDIAN_API_HOST+"/tags.json?section=music&page=%d" % (page)
            content = json.loads(urlfetch.fetch(url).content)
            for tag in content['response']['results']:
                obj = Tag.all().filter('name =',tag['webTitle']).get()
                if obj:
                    obj.name = tag['webTitle']
                    obj.guardian_id = tag['id']
                    obj.save()
                else:
                    Tag(name=tag['webTitle'],guardian_id=tag['id'], lastfm_id=tag['id']).save()
            #Get Last.fm artist names for each tag
            total = content['response']['pages']
            page += 1

    def get_guardian_articles(self):
        url = GUARDIAN_API_HOST+"/%s.json?show-fields=all&api-key=%s" % (self.guardian_id, GU_API_KEY)
        logging.info("Requesting %s", url)
        response = json.loads(urlfetch.fetch(url).content)
        logging.info("Got response: %s",response)
        return [{'headline':content["fields"]["headline"], 'trailtext':content["fields"]["trailText"], 'id':content["id"]} for content in response["response"]["results"]]
        
    