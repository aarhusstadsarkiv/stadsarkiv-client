from stadsarkiv_client.settings import settings


local_settings = {}

try:
    import settings as local_settings
    # get local settings path
    settings_type = 'local'
except ImportError:
    settings_type = 'default'
    pass

settings["settings_type"] = settings_type

# Iterate over the settings and override them with the local settings
for key, value in settings.items():
    if hasattr(local_settings, key):
        settings[key] = getattr(local_settings, key)

