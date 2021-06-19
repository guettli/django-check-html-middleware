import pytest
from django.http import HttpResponse

from check_html import CheckHTMLMiddleware, CheckHTMLException


def test_get_pre_lines_line_and_post_lines():
    assert CheckHTMLMiddleware.get_pre_lines_line_and_post_lines(['x'], 0) == ([], 'x', [])
    assert CheckHTMLMiddleware.get_pre_lines_line_and_post_lines(['a', 'b', 'c'], 1) == (['a'], 'b', ['c'])


def test_check_broken_html(rf):
    def get_response(request):
        return HttpResponse('<div>x<div>')
    try:
        CheckHTMLMiddleware(get_response)(rf.get('/'))
    except CheckHTMLException as exc:
        assert 'line 1, col 7: missing &lt;/div&gt;:' in str(exc)
    else:
        raise AssertionError('expected CheckHTMLException')

    response = CheckHTMLMiddleware(get_response)(rf.get('/admin/foo'))
    assert response.content == b'<div>x<div>'

def test_check_valid_html_content(rf):
    assert CheckHTMLMiddleware().get_errors('<div>x</div>') is None


def test_check_broken_html_content(rf):
    with pytest.raises(CheckHTMLException):
        CheckHTMLMiddleware().get_errors('<div>x<div>')


def test_settings(settings, rf):
    settings.CHECK_HTML_IGNORE_REGEX_PATH = []

    def get_response(request):
        return HttpResponse('<div>x<div>')
    with pytest.raises(CheckHTMLException):
            CheckHTMLMiddleware(get_response)(rf.get('/admin/'))
