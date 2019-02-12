"""Base class for TSBCNCUser and other related classes."""
# pylint: disable=too-many-instance-attributes

import os
import re
import shutil

try:
    from urllib import parse
except ImportError:  # above is available in py3+, below is py2.7
    import urlparse as parse

from . import constants as c
from . import urls
from . import utils


class TSBCNCUserError(Exception):
    pass



ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Base:
    """Base class for TSBC NC user- and ability-type classes. Should only
    hold common functionality for configuring state.
    """

    expected_args = (

        ('dgs_url', c.DEFAULT_DGS_URL),
        ('dgs_access_token', c.DEFAULT_DGS_ACCESS_TOKEN),

        ('ess_url', c.DEFAULT_ESS_URL),
        ('ess_access_token', c.DEFAULT_ESS_ACCESS_TOKEN),

        ('driver_name', c.DEFAULT_DRIVER_NAME),
        ('ssh_accessible', None),
        ('ssh_requires_password', None),
        ('server_user', None),
        ('server_password', None),
        ('nihilistic_wait', c.NIHILISTIC_WAIT),
        ('apathetic_wait', c.APATHETIC_WAIT),
        ('pessimistic_wait', c.PESSIMISTIC_WAIT),
        ('medium_wait', c.MEDIUM_WAIT),
        ('optimistic_wait', c.OPTIMISTIC_WAIT),
        ('quick_wait', c.QUICK_WAIT),
        ('micro_wait', c.MICRO_WAIT),
    )

    url_stdports_re = re.compile(r':(?:80|443)/?$')

    def set_url_getters(self):
        """Create functions as attributes on this instance which return needed
        URLs, given the function names and format templates defined in the urls
        module. E.g., this creates pseudo-methods like
        ``self.get_ss_login_url()``.
        """
        for base_url, url_spec in ((self.dgs_url, urls.TSBCNC_URLS),):
            for getter_name, template in url_spec:
                def getter(*args, t=template, b=base_url):
                    # Remove standard port suffix from netloc.
                    b = re.sub(self.url_stdports_re, '/', b)
                    return t.format(*(b,) + args)
                setattr(self, getter_name, getter)

    kwarg2attr_filter = {}

    def __init__(self, **kwargs):
        self.here = ROOT
        self._ss_api_key = None  # Make pylint happy.
        for kwarg, default in self.expected_args:
            setattr(self,
                    self.kwarg2attr_filter.get(kwarg, kwarg),
                    kwargs.get(kwarg, default))
        expected_kwargs = [x[0] for x in self.expected_args]
        for k, v in kwargs.items():
            if k not in expected_kwargs:
                setattr(self, k, v)
        self.set_url_getters()
        self.dummy_val = c.DUMMY_VAL
        self.cwd = None
        self._tmp_path = None
        self._permanent_path = None

    @staticmethod
    def unique_name(name):
        return '{}_{}'.format(name, utils.unixtimestamp())

    @property
    def permanent_path(self):
        if not self._permanent_path:
            self._permanent_path = os.path.join(ROOT, c.PERM_DIR_NAME)
            if not os.path.isdir(self._permanent_path):
                os.makedirs(self._permanent_path)
        return self._permanent_path

    @property
    def tmp_path(self):
        if not self._tmp_path:
            self._tmp_path = os.path.join(ROOT, c.TMP_DIR_NAME)
            if not os.path.isdir(self._tmp_path):
                os.makedirs(self._tmp_path)
        return self._tmp_path

    def clear_tmp_dir(self):
        for thing in os.listdir(self.tmp_path):
            thing_path = os.path.join(self.tmp_path, thing)
            if os.path.isfile(thing_path):
                os.unlink(thing_path)
            elif os.path.isdir(thing_path):
                shutil.rmtree(thing_path)

    @property
    def dgs_hostname(self):
        return parse.urlparse(self.dgs_url).hostname
