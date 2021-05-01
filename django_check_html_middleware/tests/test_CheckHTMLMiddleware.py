from django_check_html_middleware import CheckHTMLMiddleware


def test_get_pre_lines_line_and_post_lines():
    assert CheckHTMLMiddleware.get_pre_lines_line_and_post_lines(['x'], 0) == ([], 'x', [])
    assert CheckHTMLMiddleware.get_pre_lines_line_and_post_lines(['a', 'b', 'c'], 1) == (['a'], 'b', ['c'])


