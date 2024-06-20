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
    │   ├── css
    │   │   └── local.css
    │   └── js
    │       ├── home.js
    │       └── local.js
    └── templates
        ├── auth
        │   └── login.html
        ├── includes
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

## Templates

### Override

Templates that you can override can be found in the [stadsarkiv_client/templates](/stadsarkiv_client/templates) directory. In order to override a template you place your custom template in the `templates` directory. In the `example-config-simple` there is a override of `auth/login.html`.

There is also an override of the `home.html`. As you can see in this template, you may add custom css and js files in the `head` block. This is done like this: 

```html
{% block head %}
<script src="{{ url_for('static', path='/js/home.js') }}"></script>
{% endblock head %}
```

Using the above code you may add custom css and js files to the `head` block of any individual template.

### Custom pages

You may add custom pages. In the `example-config-simple` there is a custom page `searchguide.html`. You may add custom pages anywhere in the `templates` directory. In the above example the custom page is placed in `templates/pages/searchguide.html`.

## Static files

You may also override any static file found in [stadsarkiv_client/static](/stadsarkiv_client/static)

An easier way to add custom css and js is just to create a `css/local.css` and `css/local.js` file. These files are loaded in the base templates if they exist. They are loaded just before the closing `</head>` tags. 








