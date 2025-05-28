import re

def is_valid_url(url):
    pattern = re.compile(
        r'^https?:\/\/[\w\-\.]+(\.[a-z]{2,6})?\/?.*$', re.IGNORECASE
    )
    return bool(pattern.match(url))