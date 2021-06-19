# django-check-html-middleware

This middleware for the Django Web Frameworks checks the HTML you create.

The middleware should only be used during development.

By default the middleware deactivates itself, if settings.DEBUG is False.

# In Action

Imagine you have a typo in your HTML like this: `<th>foo</td>`, then you get a html page like this:

```
line 89, col 14: discarding unexpected </td>:
      <th>foo</td>
```

# Anachronism?

Many people send JSON instead of HTML over the wire these days....

I use [htmx](//htmx.org) and function-based-views if I can choose :-)

# Install
```
pip install django-check-html-middleware
```

# settings.py

Add `check_html.CheckHTMLMiddleware` at the start of your middleware.

If you use the Django-Debug-Toolbar, then put the check-html middleware below it.

```
MIDDLEWARE = [
    'check_html.CheckHTMLMiddleware',
    ....
]
```

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

CHECK_HTML_IGNORE_REGEX_PATH: A list of regex strings. If a URL path matches this string, this response
does not get checked.

Defaults to:
```
[
    '/admin/.*',
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
