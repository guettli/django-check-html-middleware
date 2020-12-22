from django.conf import settings
from django.core.exceptions import MiddlewareNotUsed
from django.http import HttpResponseServerError
from django.utils.html import format_html, conditional_escape
from django.utils.safestring import mark_safe


def join(my_list, sep=''):
    return mark_safe(sep.join([conditional_escape(item) for item in my_list]))

class CheckHTMLMiddleware():
    ignore_messages = (
        'trimming empty',
    )
    def __init__(self, get_response):
        if not settings.DEBUG:
            raise MiddlewareNotUsed()
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.streaming:
            return response
        import tidy
        doc = tidy.parseString(response.content)
        if not doc.errors:
            return response
        return self.create_error_report(doc, response.content, response)

    def skip_this_error(self, error):
        for msg in self.ignore_messages:
            if msg in error.message:
                return True

    def create_error_report(self, doc, content, response):
        lines = content.split(b'\n')
        errors_html = []
        for error in doc.errors:
            if self.skip_this_error(error):
                continue
            line = lines[error.line-1]
            errors_html.append(format_html('<li>line {}, col {}: {}: <pre>{}</pre>', error.line, error.col, error.message, line.decode('utf8')))
        if not errors_html:
            return response
        return HttpResponseServerError(format_html('<ul>{}</ul>', join(errors_html)))


