# django-check-html-middleware

This middleware for the Django Web Frameworks checks the HTML you create.

The middleware should only be used during development.

By default the middleware deactivates itself, if settings.DEBUG is False.

# Install
```
pip install django-check-html-middleware
```

# settings.py

CHECK_HTML_IGNORE_MESSAGES: A list of strings. Each string is an error messages which should get ignored.

Defaults to:
```
[
    'trimming empty',
    'proprietary attribute',
    'missing <!DOCTYPE> declaration',
    'inserting implicit <body>',
    '''inserting missing 'title' element''',
    'moved <style> tag to <head>',
    'inserting implicit <p>',
    ]
```

CHECK_HTML_IGNORE_STARTSWITH_PATH: A list of strings. If a URL path starts with this string, this response
does not get checked.

Defaults to:
```
[
    '/admin/',
    ]
```

# Wrapper for "utidylib"

This middleware is just a thin wrapper for [utidylib](https://pypi.org/project/uTidylib/).

# Feedback is welcome!

What do you think could get improved?

Please tell me and open an issue at github.

Thank you!

# Development installation

```
python3 -m venv check-html-env
cd check-html-env/
. bin/activate
pip install -U pip wheel
git clone git@github.com:guettli/django-check-html-middleware.git
mv django-check-html-middleware code
pip install -e code
cd code

pytest
```