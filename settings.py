# Put your Guardian Content API key here
GU_API_KEY=""
# If you signed a commercial agreement, you can set this to True to get pictures and no ads
IS_PARTNER=False
# For guardian devs who can run the Content API locally (and therefore offline say on the train)
IS_LOCAL_API=False

# If you get this from github, the settings_local.py wont exist, 
# copy the settings here and put them in to not distribute your API keys when you republish the source
try:
    from settings_local import *
except ImportError:
    pass