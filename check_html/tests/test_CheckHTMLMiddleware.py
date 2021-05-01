from django.http import HttpResponse

from check_html import CheckHTMLMiddleware, CheckHTMLException


def test_get_pre_lines_line_and_post_lines():
    assert CheckHTMLMiddleware.get_pre_lines_line_and_post_lines(['x'], 0) == ([], 'x', [])
    assert CheckHTMLMiddleware.get_pre_lines_line_and_post_lines(['a', 'b', 'c'], 1) == (['a'], 'b', ['c'])


def test_check_html(rf):
    def get_response(request):
        return HttpResponse('<div>x<div>')
    try:
        CheckHTMLMiddleware(get_response)(rf.get('/'))
    except CheckHTMLException as exc:
        assert 'line 1, col 7: missing &lt;/div&gt;:' in str(exc)

    response = CheckHTMLMiddleware(get_response)(rf.get('/admin/'))
    assert response.content == b'<div>x<div>'
