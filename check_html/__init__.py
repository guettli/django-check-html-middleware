import os
import re
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
        '<img> lacks "alt" attribute',
    )

    ignore_regex_paths: List[str]

    ignore_regex_paths_default = [
        '/admin/.*',
    ]

    def __init__(self, get_response=None):
        if not (settings.DEBUG or 'PYTEST_CURRENT_TEST' in os.environ):
            raise MiddlewareNotUsed()
        self.get_response = get_response
        self.ignore_messages = getattr(settings, 'CHECK_HTML_IGNORE_MESSAGES', self.ignore_messages_default)
        self.ignore_regex_paths = getattr(settings, 'CHECK_HTML_IGNORE_REGEX_PATH',
                                               self.ignore_regex_paths_default)


    def skip_path(self, path):
        for regex in self.ignore_regex_paths:
            if re.match(regex, path):
                return True
        return False

    def __call__(self, request):
        response = self.get_response(request)
        if request.GET and request.GET.get('nocheck'):
            return response
        content_type = response.get('content-type', '')
        if not content_type.startswith('text/html'):
            return response
        if b'ul.traceback' in response.content: # django debug page
            return response
        if self.skip_path(request.path):
            return response
        if response.streaming:
            return response
        if not response.content:
            return response
        errors_html = self.get_errors(response.content, url=request.build_absolute_uri())
        if not errors_html:
            return response
        return HttpResponseServerError(errors_html)

    def get_errors(self, content, url=''):
        if isinstance(content, str):
            content = content.encode('utf8')
        import tidy
        doc = tidy.parseString(content)
        if not doc.errors:
            return
        return self.create_error_report(doc, content, url)

    def skip_this_error(self, error):
        for msg in self.ignore_messages:
            if msg in error.message:
                return True

    def create_error_report(self, doc, content, url=''):
        lines = [line.decode('utf8') for line in content.split(b'\n')]
        errors_html = []
        for error in doc.errors:
            if self.skip_this_error(error):
                continue
            errors_html.append(format_html('<li>line {}, col {}: {}: {}', error.line, error.col, error.message,
                                           self.lines_html(lines, error.line-1)))
        if not errors_html:
            return
        errors_html = format_html('<ul>{}</ul>', join(errors_html))
        if "PYTEST_CURRENT_TEST" in os.environ:
            raise CheckHTMLException('at {}: {}', url, errors_html)
        return errors_html

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
