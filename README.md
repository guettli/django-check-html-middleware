# What is "django-check-html-middleware"?

This middleware for the Django Web Frameworks provides you a way to check all HTML which you create 
on the server before sending it to the client.

It get created to check HTML during development an testing. At least I don't use it on production servers.

By default the middleware deactivates itself, if settings.DEBUG is False.

# Development installation

```
pip install -e git+ssh://git@github.com/guettli/django-check-html-middleware.git#egg=django-check-html-middleware
```