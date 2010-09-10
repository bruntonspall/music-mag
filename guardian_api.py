import logging
import urllib
from google.appengine.api import urlfetch

try:
    import json
except ImportError:
    from django.utils import simplejson as json

from settings import *

if IS_LOCAL_API:
    GUARDIAN_API_HOST = 'http://localhost:8700/content-api/api'
else:
    GUARDIAN_API_HOST = 'http://content.guardianapis.com'

API_URL = "%(host)s/%(path)s?%(args)s"

def make_request(path, args):
    args['api-key'] = GU_API_KEY
    if IS_LOCAL_API:
        if IS_PARTNER:
            args["userTier"]="partner"
        else:
            args["userTier"]="approved"
    url = API_URL % {"host":GUARDIAN_API_HOST, "path":path, "args":urllib.urlencode(args)}
    logging.info("Requesting %s" % url)
    response = urlfetch.fetch(url)
    return response.content

def get_json(path, args):
    args['format'] = 'json'
    return json.loads(make_request(path, args))

def get_content_for_guardian_id(id):
    args = {"show-fields":"all"}
    if IS_PARTNER:
        args["show-media"]="picture"
    response = get_json(id, args)

    content = response["response"]["content"]
    image = None
    if content.has_key('mediaAssets'):
        image = content["mediaAssets"][0]["file"]
    return {'headline':content["fields"]["headline"], 'trailtext':content["fields"]["trailText"],'body':content["fields"]["body"], 'image':image,'id':content["id"]}

def get_guardian_articles(tag):
    response = get_json(tag, {"show-fields":"headline,trailText"})
    return [{'headline':content["fields"]["headline"],
             'trailtext':content["fields"]["trailText"],
             'id':content["id"]} for content in response["response"]["results"]]

def get_tags(section="music", page=None):
    args = {"section":section}
    if page:
        args['page'] = page
    return get_json('tags', args)
