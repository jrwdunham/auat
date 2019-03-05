import os


def internalize_url(url):
    mapping = os.getenv('URL_INTERNALIZE_MAPPING')
    if mapping:
        k, v = mapping.split('|')
        return url.replace(k, v)
    return url
