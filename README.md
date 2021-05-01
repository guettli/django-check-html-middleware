# What is "django-check-html-middleware"?

This middleware for the Django Web Frameworks provides you a way to check all HTML which you create 
on the server before sending it to the client.

It get created to check HTML during development an testing. At least I don't use it on production servers.

By default the middleware deactivates itself, if settings.DEBUG is False.

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