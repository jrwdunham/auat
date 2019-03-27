from collections import namedtuple
import os


def internalize_url(url):
    mapping = os.getenv('URL_INTERNALIZE_MAPPING')
    if mapping:
        k, v = mapping.split('|')
        return url.replace(k, v)
    return url


# A "recipe" deterministically defines how to generate a document of type otype
# from template using context.
Recipe = namedtuple('Recipe', 'template, context, otype')
