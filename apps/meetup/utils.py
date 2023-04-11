from __future__ import annotations

cookie_name = 'moscowdjango_vote'


def can_vote(request):
    return not request.COOKIES.get(cookie_name, None)


def set_vote_cookie(response):
    response.set_cookie(cookie_name, 'done')
    return response
