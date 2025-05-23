# Client

A custom `maya` client is generated by overriding `templates`, `static` files, `.env`, and `settings` files. E.g. it may look something like this:

    sites/simple/
    ├── .env
    ├── facets.yml
    ├── hooks.py
    ├── language.yml
    ├── settings.yml
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
        │   └── head_extra.html
        └── pages
            ├── collections.html
            ├── home.html
            └── searchguide.html

The above structure shows the `sites/simple` client. You may use this client as a starting point. You can browse the files of the client by visiting this link: [sites/simple](https://github.com/aarhusstadsarkiv/maya/tree/main/sites/simple).

Run the client:

```bash
maya server-dev sites/simple
```

## .env

In `.env` you may set the following:

```ini
# API_KEY is required for the client to work. You may request an API key from Aarhus Stadsarkiv.
API_KEY=your_api_key

# SESSION Secret
SECRET=some_secret

# development or production
# If ENVIRONMENT is set to production, the log level is INFO
# If ENVIRONMENT is set to development, the log level is DEBUG
ENVIRONMENT=development
```

You may generate a new secret using the following command:

```bash
maya server-secret
```

## language.yml

In `language.yml` you may override translations:

```yml
Forgot your password: Glemt password (Fra local language.yml)
```

Original language files (and keys) can be found in [maya/locales/da.yml](https://github.com/aarhusstadsarkiv/maya/blob/main/maya/locales/da.yml)

## Templates

### Override

Templates that you can override can be found in the [maya/templates](https://github.com/aarhusstadsarkiv/maya/blob/main/maya/templates) directory. In order to override a template you place your custom template in the `templates` directory. In the `sites/simple` there is a override of `auth/login.html` and `pages/home.html`.

As you can see in the home.html template, you may add custom css and js files in the `head` block. This is done like this:

```html
{% block head %}
<script src="{{ url_for('static', path='/js/home.js') }}"></script>
{% endblock head %}
```

The above code adds custom css or js files to the `head` block of any individual template.

You may also add custom css and js files to the `head` block of all templates. This is done by overriding `templates/includes/head_extra.html`. In the `sites/simple` there is a custom `head_extra.html` file that just adds a log message to the browser console.

An easy way to alter the footer is to override the `templates/includes/footer.html`.

### Custom pages

You may add custom pages. In the `sites/simple` there is a custom page `searchguide.html`. You may add custom pages anywhere in the `templates` directory. In the above example the custom page is placed in `templates/pages/searchguide.html`. These pages needs to be added to a `settings` file in order to be accessible and active. 

## Static files

### Override

You may also override any static file found in [maya/static](https://github.com/aarhusstadsarkiv/maya/blob/main/maya/static)

E.g. if you only want to alter the `logo` and the `favicon` you need to create a `static/assets/default_logo.png` and `static/assets/favicon.ico` in your `sites/simple` directory.

If you just want to change the color scheme you can create a `static/assets/css/light.css` file. Here are all the colors of the default theme defined. You may override any of them.

An easy way to add custom css and js is just to create a `static/assets/css/local.css` and `static/assets/js/local.js` file. These files are loaded in the base templates if they exist. The css file is loaded as the last css file in the `head` block. The js file is loaded as the last js file in the `head` block.

## Settings

There are quite a few settings. In order to view all base settings you can go to the [sites/simple/settings.yml](https://github.com/aarhusstadsarkiv/maya/blob/main/sites/simple/settings.yml) file. This file is quite well documented.

Another settings file is [sites/simple/facets.yml](https://github.com/aarhusstadsarkiv/maya/blob/main/sites/simple/facets.yml). This file is used to define the facets that are shown on the search page. You may add, remove, or change the order of the facets. 

If the `facets.yml` file does not exist, the default facets are used. 

In the settings.yml file you can specify which of the default facets are enabled. In the `sites/simple` it is `[content_types, events, dates]`. If a local facets.yml file exists then these facets will override the default facets.

If you look at the `type` of each facet section you will notice that there are three types: 

1. `default`. This extends the `current search` when the user select a new facet. 
2. `resource_links`. These are links to a resouce, e.g. a `person` or `event` etc. 
3. `date_form`. This type is used for display dates, which can alter the search results according to dates.

## Hooks

In the `hooks.py` file you may do some custom actions. In the [sites/simple/hooks.py](https://github.com/aarhusstadsarkiv/maya/blob/main/sites/simple/hooks.py) you can see all the hooks available. 
