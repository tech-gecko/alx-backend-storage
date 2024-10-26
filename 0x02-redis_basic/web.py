#!/usr/bin/env python3
from datetime import timedelta
import redis
import requests


def get_page(url: str) -> str:
    """Obtains the HTML content of a particular URL and returns it."""
    r = redis.Redis()

    r.set(f'count:{url}', 0)

    if not r.exists(f'html:{url}'):
        html = requests.get(url).text
        r.setex(
            f'html:{url}',
            timedelta(seconds=10),
            html
        )
        r.incr(f'count:{url}')

    html = r.get(f'html:{url}').decode('utf-8')

    return html
