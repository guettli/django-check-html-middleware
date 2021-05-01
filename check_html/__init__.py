import os
from typing import List

from django.conf import settings
from django.core.exceptions import MiddlewareNotUsed
from django.http import HttpResponseServerError
from django.utils.html import format_html, conditional_escape
from django.utils.safestring import mark_safe


def join(my_list, sep=''):
    return mark_safe(sep.join([conditional_escape(item) for item in my_list]))

class CheckHTMLException(Exception):
    pass

class CheckHTMLMiddleware():
    ignore_messages: List[str]

    ignore_messages_default = (
        'trimming empty',
        'proprietary attribute',
        'missing <!DOCTYPE> declaration',
        'inserting implicit <body>',
        '''inserting missing 'title' element''',
        'moved <style> tag to <head>',
        'inserting implicit <p>',
    )

    ignore_startswith_paths: List[str]

    ignore_startswith_paths_default = [
        '/admin/',
    ]

    def __init__(self, get_response):
        if not settings.DEBUG:
            raise MiddlewareNotUsed()
        self.get_response = get_response
        self.ignore_messages = getattr(settings, 'CHECK_HTML_IGNORE_MESSAGES', self.ignore_messages_default)
        self.ignore_startswith_paths = getattr(settings, 'CHECK_HTML_IGNORE_STARTSWITH_PATH',
                                               self.ignore_startswith_paths_default)


    def skip_path(self, path):
        for startswith in self.ignore_startswith_paths:
            if path.startswith(startswith):
                return True
        return False

    def __call__(self, request):
        response = self.get_response(request)
        if request.GET and request.GET.get('nocheck'):
            return response
        if not response['content-type'].startswith('text/html'):
            return response
        if b'ul.traceback' in response.content: # django debug page
            return response
        if self.skip_path(request.path):
            return response
        if response.streaming:
            return response
        if not response.content:
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
        lines = [line.decode('utf8') for line in content.split(b'\n')]
        errors_html = []
        for error in doc.errors:
            if self.skip_this_error(error):
                continue
            errors_html.append(format_html('<li>line {}, col {}: {}: {}', error.line, error.col, error.message,
                                           self.lines_html(lines, error.line-1)))
        if not errors_html:
            return response
        if "PYTEST_CURRENT_TEST" in os.environ:
            raise CheckHTMLException(errors_html)
        return HttpResponseServerError(format_html('<ul>{}</ul>', join(errors_html)))

    @classmethod
    def lines_html(cls, lines, error_index):
        pre, line, post = cls.get_pre_lines_line_and_post_lines(lines, error_index)
        return format_html('''
        <pre>{}</pre>
        <pre style="font-weight: bold">{}</pre>
        <pre>{}</pre>''', '\n'.join(pre), line, '\n'.join(post))

    @classmethod
    def get_pre_lines_line_and_post_lines(cls, lines, error_index, lines_before=5):
        line = lines[error_index]
        pre = lines[max(error_index - lines_before, 0):error_index]
        post = lines[error_index+1:min(error_index + lines_before, len(lines))]
        return pre, line, post
