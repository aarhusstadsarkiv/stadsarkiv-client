# Client

A new client is overriding the default client files. 

This is a simple example of a client. 

    example-config-simple
    ├── .env
    ├── hooks.py
    ├── language.py
    ├── settings_facets.py
    ├── settings.py
    ├── static
    │   └── js
    │       └── hello_world.js
    └── templates
        └── pages
            └── home.html

## .env

In `.env` you may set the following:

```ini
# SESSION Secret
SECRET=SECRET

# development or production
# If ENVIRONMENT is set to production, the log level is INFO
# If ENVIRONMENT is set to development, the log level is DEBUG
ENVIRONMENT=development
```

You may generate a new secret using the following command:

```bash
stadsarkiv-client server-secret
```

## language.py

In `language.py` you may override translations:

```python
# This file overrides translation keys.
language = {
    "Forgot your password": "Har du glemt dit kodeord?",
}
```

Original language files (and keys) may be found in [stadsarkiv_client/locales/da.py](stadsarkiv_client/locales/da.py)





