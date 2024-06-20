# Client

A new client is overriding the default client files. 

This is a simple example of a client. You may override the following files and directories:

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
        ├── auth
        │   └── login.html
        └── pages
            ├── collections.html
            ├── home.html
            └── searchguide.html

You may run the above client using the following command:

```bash
stadsarkiv-client server-dev -c example-config-simple
```

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

Original language files (and keys) may be found in [stadsarkiv_client/locales/da.py](/stadsarkiv_client/locales/da.py)

## templates

**Override templates**

In `templates` you may add `custom pages` and override existing templates. The templates that you can override can be
found in the [stadsarkiv_client/templates](/stadsarkiv_client/templates) directory. In order to override you place your
custom template in the `templates` directory. In the `example-config-simple` there is a override of `auth/login.html`.

**Add custom pages**

You may add custom pages. In the `example-config-simple` there is a custom page `searchguide.html`. You may add custom
anywhere in the `templates` directory. In the above example the custom page is placed in `templates/pages/searchguide.html`.

## static

You may also add custom css files. In the `example-config-simple` there is a custom `custom.css` file placed in `static/css/custom.css`. 

As with templates you may add custom static files. In the `example-config-simple` there is a custom `hello_world.js` file
placed in `static/js/hello_world.js`. You may add custom static files anywhere in the `static` directory. 






