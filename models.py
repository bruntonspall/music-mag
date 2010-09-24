#!/usr/bin/env python
# encoding: utf-8
"""
models.py

Created by MBS on 2010-08-13.
"""
from google.appengine.ext import db

class Tag(db.Model):
    name = db.StringProperty(required=True)
    lname = db.StringProperty(required=True)
    guardian_id = db.StringProperty(required=True)
    lastfm_id = db.StringProperty(required=True)

    def __init__(self, *args, **kwargs):
        kwargs['lname'] = kwargs['name'].lower()
        db.Model.__init__(self, *args, **kwargs)
            
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
