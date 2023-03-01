from stadsarkiv_client.settings import settings

settings_local = {}

try:
    from settings_local import settings_local
except ImportError:
    pass


for key, value in settings_local.items():
    settings[key] = value
