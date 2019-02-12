# Default values
# =========================================================================


DEFAULT_DGS_URL = 'http://127.0.0.1:61780/micros/dgs/v1/api/'
DEFAULT_DGS_ACCESS_TOKEN = 'nope'

DEFAULT_ESS_URL = 'http://127.0.0.1:61780/micros/ess/v1/api/'
DEFAULT_ESS_ACCESS_TOKEN = 'nope'

DEFAULT_DRIVER_NAME = 'Chrome'  # 'Firefox' should also work.
DUMMY_VAL = 'some value'
TMP_DIR_NAME = '.tsbc-nc-tmp'
PERM_DIR_NAME = 'data'

# Waits and Timeouts
# =========================================================================
#
# Note that there is redundancy between this and the configuration in
# features/environment.py. These values are specified here also so that
# ``TSBCNCUser`` can technically remain independent of its use within a
# ``behave`` feature-running context. The proper way to customize these values
# when using ``behave`` is to use Behave "user data" flags, e.g.,
# ``behave -D nihilistic_wait=30``.

# Generable, reusable wait times, in seconds
NIHILISTIC_WAIT = 20
APATHETIC_WAIT = 10
PESSIMISTIC_WAIT = 5
MEDIUM_WAIT = 3
OPTIMISTIC_WAIT = 1
QUICK_WAIT = 0.5
MICRO_WAIT = 0.25
