import logging
import os

import user


ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Change these to match your test environment
# These may also be overridden as Behave userdata options
# (https://pythonhosted.org/behave/new_and_noteworthy_v1.2.5.html#index-7),
# i.e., ``behave -D dgs_url=https://... -D dgs_access_token=secret``
DGS_URL = 'http://127.0.0.1:61780/micros/dgs/v1/api/'
DGS_ACCESS_TOKEN = 'nope'
ESS_URL = 'http://127.0.0.1:61780/micros/ess/v1/api/'
ESS_ACCESS_TOKEN = 'nope'
DES_URL = 'http://127.0.0.1:61780/micros/des/v1/api/'
DES_ACCESS_TOKEN = 'nope'
DES_INBOX_PATH = '/var/lib/desdata/inbox/'

DRIVER_NAME = 'Chrome'

# Set these constants if the TSBC NC client should be able to gain SSH access to the
# server where the TSBC NC APIs are being served. This is needed in order to scp server files
# to local, which some tests need. If SSH access is not possible, set
# ``SSH_ACCESSIBLE`` to ``False``.
SSH_ACCESSIBLE = True
SSH_REQUIRES_PASSWORD = True
SSH_IDENTITY_FILE = None
SERVER_USER = 'vagrant'
SERVER_PASSWORD = 'vagrant'

# Generable, reusable wait times, in seconds
NIHILISTIC_WAIT = 20
APATHETIC_WAIT = 10
PESSIMISTIC_WAIT = 5
MEDIUM_WAIT = 3
OPTIMISTIC_WAIT = 1
QUICK_WAIT = 0.5
MICRO_WAIT = 0.25


def str2bool(thing):
    if isinstance(thing, bool):
        return thing
    if thing.strip().lower() in ('true', 'y', 'yes', '1'):
        return True
    return False


def get_des_inbox_accessible(val):
    if isinstance(val, bool):
        return val
    return val.lower() in ('true', 'yes', 'y', 't', '1')


def get_tsbc_nc_user(userdata):
    """Instantiate a TSBCNCUser."""
    userdata.update({
        'dgs_url': userdata.get('dgs_url', DGS_URL),
        'dgs_access_token': userdata.get('dgs_access_token', DGS_ACCESS_TOKEN),
        'ess_url': userdata.get('ess_url', ESS_URL),
        'ess_access_token': userdata.get('ess_access_token', ESS_ACCESS_TOKEN),
        'des_url': userdata.get('des_url', DES_URL),
        'des_access_token': userdata.get('des_access_token', DES_ACCESS_TOKEN),
        'des_inbox_accessible': get_des_inbox_accessible(
            userdata.get('des_inbox_accessible', False)),
        'des_inbox_path': userdata.get('des_inbox_path', DES_INBOX_PATH),
        'tester_email': userdata.get('tester_email', None),
        'tester_email_password': userdata.get(
            'tester_email_password',
            os.environ.get('TSBC_NC_AUAT_TESTER_EMAIL_PASSWORD')),
        'clean_up': str2bool(userdata.get('clean_up', 'true')),
        'driver_name': userdata.get('driver_name', DRIVER_NAME),
        'ssh_accessible': bool(
            userdata.get('ssh_accessible', SSH_ACCESSIBLE)),
        'ssh_requires_password': bool(
            userdata.get('ssh_requires_password', SSH_REQUIRES_PASSWORD)),
        'server_user': userdata.get('server_user', SERVER_USER),
        'server_password': userdata.get('server_password', SERVER_PASSWORD),
        'ssh_identity_file': userdata.get(
            'ssh_identity_file', SSH_IDENTITY_FILE),
        # User-customizable wait values:
        'nihilistic_wait': userdata.get('nihilistic_wait', NIHILISTIC_WAIT),
        'apathetic_wait': userdata.get('apathetic_wait', APATHETIC_WAIT),
        'pessimistic_wait': userdata.get('pessimistic_wait', PESSIMISTIC_WAIT),
        'medium_wait': userdata.get('medium_wait', MEDIUM_WAIT),
        'optimistic_wait': userdata.get('optimistic_wait', OPTIMISTIC_WAIT),
        'quick_wait': userdata.get('quick_wait', QUICK_WAIT),
        'micro_wait': userdata.get('micro_wait', MICRO_WAIT),
    })
    return user.TSBCNCUser(**userdata)


def before_all(context):
    logging_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    context.config.setup_logging(format=logging_format)
    logger = logging.getLogger('environment')
    log_filename = 'TSBC-NC-AUAT.log'
    root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    log_path = os.path.join(root_path, log_filename)
    file_handler = logging.FileHandler(log_path)
    file_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(logging_format)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


def before_scenario(context, scenario):
    """Instantiate an ``TSBCNCUser`` instance."""
    userdata = context.config.userdata
    context.user = get_tsbc_nc_user(userdata)


def after_scenario(context, scenario):
    """Do some clean up after each scenario is run."""
    if context.user.clean_up:
        context.user.clear_tmp_dir()
