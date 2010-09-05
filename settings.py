GU_API_KEY=

# If you get this from github, the settings_local.py wont exist, copy the settings here and put them in to not distribute your API keys
try:
    from settings_local import *
except ImportError:
    pass