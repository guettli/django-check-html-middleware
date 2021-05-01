from django.http import HttpResponse

from check_html import CheckHTMLMiddleware


def test_get_pre_lines_line_and_post_lines():
    assert CheckHTMLMiddleware.get_pre_lines_line_and_post_lines(['x'], 0) == ([], 'x', [])
    assert CheckHTMLMiddleware.get_pre_lines_line_and_post_lines(['a', 'b', 'c'], 1) == (['a'], 'b', ['c'])


def test_check_html(mocker):
    response = HttpResponse('<div>x<div>')
    assert 0, mocker.patch(CheckHTMLMiddleware, 'get_response', response)