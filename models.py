#!/usr/bin/env python
# encoding: utf-8
"""
models.py

Created by MBS on 2010-08-13.
Copyright (c) 2010 __MyCompanyName__. All rights reserved.
"""
from google.appengine.ext import db

import logging
from google.appengine.api.labs import taskqueue

class Tag(db.Model):
    name = db.StringProperty(required=True)
    guardian_id = db.StringProperty(required=True)
    lastfm_id = db.StringProperty(required=True)
            
class Page(db.Model):
    edition = db.IntegerProperty(required=True)
    number = db.IntegerProperty(required=True)
    guardian_article_id = db.StringProperty(required=False)
    headline = db.StringProperty(required=True)
    trailtext = db.StringProperty(required=True)
    body = db.TextProperty(required=True)
    image = db.StringProperty(required=False)
    

class KVStore(db.Expando):
    name = db.StringProperty(required=True)