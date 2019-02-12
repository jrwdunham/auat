"""Utilities for TSBC NC User."""

import logging
import time

import requests

from . import constants as c


logger = logging.getLogger('user.utils')


def squash(string_):
    """Simple function that makes it easy to compare two strings for
    equality even if they have incidental (for our purposes) formatting
    differences.
    """
    return string_.strip().lower().replace(' ', '')


def is_uuid(idfr):
    """Return true if ``idfr`` is a UUID."""
    return (
        [8, 4, 4, 4, 12] == [
            len([x for x in y if x in '1234567890abcdef'])
            for y in idfr.split('-')])


def unixtimestamp():
    return int(time.time())


def all_urls_resolve(urls):
    """Return ``True`` only if all URLs in ``urls`` return good status codes
    when GET-requested.
    """
    for purl in urls:
        r = requests.get(purl)
        if r.status_code != 200:
            return False
    return True
