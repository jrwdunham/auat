TSBC NC Automated User Acceptance Tests (TSBC-NC-AUAT)
================================================================================

This repository contains automated user acceptance tests for the TSBC NC APIs
written using the Python behave_ library and the Gherkin_ language. Using
Gherkin to express tests makes them readable to a wide range of TSBC
users and stakeholders [1]_. Consider the following snippet from the *AR OP
Consolidated Email Generation* feature file (``core.feature``)::

    Feature: AR OP Consolidated HTML Email Generation
      Clients of the TSBC NC APIs want to be able to generate HTML email documents
      using the Email Sending Service (ESS).

      Scenario Outline: Dan wants to generate the Accounts Receivable (AR) Operating Permit (OP) renewal HTML email documents using the DGS and confirm that the generated documents have the expected properties.
        Given a DGS instance containing the production templates
        When a document is generated from template <template_key> using data context <context_path>
        Then the generated document is stored in the MDS
        AND the generated document is rendered correctly

        Examples: templates and contexts
        | template_key                               | context_path                                                |
        | ar_op_friendly_reminder_consolidated_email | etc/test_contexts/ar-op-friendly-reminder-consolidated.json |

The ``Given``, ``When`` and ``Then`` statements in the feature files allow us
to put the system into a known state, perform user actions, and then make
assertions about the expected outcomes, respectively. These steps are
implemented by *step* functions in Python modules located in the
``features/steps/`` directory, which, in turn, may interact with TSBC NC
APIs by calling methods of a ``TSBCNCUser`` instance as defined in the ``user``
package. For detailed guidance on adding feature files, implementing steps, or
adding user abilities, please see the `Developer documentation
<docs/developer-documentation.rst>`_. For examples of using these tests to run
(performance) experiments on TSBC APIs, see `Running Experiments with the
TSBC-NC-AUAT <docs/running-experiments.rst>`_.


Table of Contents
--------------------------------------------------------------------------------

- `High-level overview`_
- `Installation`_
- `Usage`_


High-level overview
================================================================================

The TSBC-NC-AUAT are a completely separate application the various TSBC NC APIs.
They require that you already have instances of these APIs deployed somewhere
(locally or publicly) that you can test against (see
`Installing TSBC NC APIs`_.) The tests must be supplied with configuration
details, including crucially the URLs and access tokens of the services that
will be used (e.g., DGS, ESS). The service instances being tested may be
running locally on the same machine or remotely on an external server. Note
that running all of the TSBC-NC-AUAT tests to completion may take some time.


Installation
================================================================================

This section describes how to install the TSBC-NC-AUAT. If you have done this before
and just need a refresher, see the `Installation quickstart`_. If you are
installing manually for the first time, see the `Detailed installation
instructions`_. If you are testing a local deploy created using `nc`_ (Docker
Compose), then the tests should be installed for you automatically.


Installation quickstart
--------------------------------------------------------------------------------

The following list of commands illustrates the bare minimum required in order
to install and run the tests. Note that a real-world invocation of the
``behave`` command will require the addition of flags that are particular to
your environment and the details of the API instances that you are
testing against (see Usage_). If you have never run these tests before, please
read the `Detailed installation instructions`_ first.::

    $ python -m venv venv
    $ source venv/bin/activate
    $ git clone https://jdunham@bitbucket.safetyauthority.ca/scm/nc/tsbc-nc-auat.git
    $ cd tsbc-nc-auat
    $ pip install -r requirements.txt
    $ behave


Detailed installation instructions
--------------------------------------------------------------------------------

To install these tests manually, first create a virtual environment using Python
3 and activate it::

    $ python -m venv venv
    $ source venv/bin/activate

Then clone the source::

    $ git clone https://jdunham@bitbucket.safetyauthority.ca/scm/nc/tsbc-nc-auat.git

Finally, install the Python dependencies::

    $ pip install -r requirements.txt


Installing the TSBC NC APIs
--------------------------------------------------------------------------------

As mentioned previously, running the TSBC-NC-AUAT requires having existing
TSBC NC API instances deployed. Describing how to do this is beyond the
scope of this document. Using the Docker Compose strategy is the recommended
method for deploying the TSBC NC APIs locally for development and testing. See
the following link:

- `Docker Compose`_ TSBC NC APIs Docker Compose local install and deploy


Usage
================================================================================

Simply executing the ``behave`` command will run all of the tests and will use
the default URLs and access tokens defined in
``features/environment.py``. However, in the typical case you will need to
provide Behave with some configuration details that are appropriate to your
environment and which target a specific subset of tests (i.e., feature files or
scenarios).  The following command is a more realistic example of running the
TSBC-NC-AUAT::

    $ behave \
        --tags=generate-ar-op-cons-emails \
        --no-skipped \
        -v \
        --stop \
        -D dgs_url=http://127.0.0.1:61780/micros/dgs/v1/api/ \
        -D dgs_access_token=<DGS_TOKEN> \
        -D ess_url=http://127.0.0.1:61780/micros/ess/v1/api/ \
        -D ess_access_token=<ESS_TOKEN> \
        -D driver_name=Firefox

The command given above is interpreted as follows.

- The ``--tags=generate-ar-op-cons-emails`` flag tells Behave that we only want
  to run the *AR OP Consolidated HTML Email Generation* feature as defined in the
  ``features/core/core.feature`` file, which has the
  ``@generate-ar-op-cons-emails`` tag.
- The ``--no-skipped`` flag indicates that we do not want the output to be
  cluttered with information about the other tests (feature files) that we are
  skipping in this run.
- The ``-v`` flag indicates that we want verbose output, i.e., that we want any
  print statements to appear in stdout.
- The ``--stop`` flag tells Behave to stop running the tests as soon as there
  is a single failure.
- The rest of the ``-D``-style flags are Behave *user data*:

  - The ``-D driver_name=Firefox`` flag tells Behave to use the Firefox browser.
  - Finally, the remaining user data flags provide Behave with the URLs and
    authentication details of particular TSBC NC API instances.

To see all of the Behave user data flags that the TSBC-NC-AUAT recognizes, inspect the
``get_tsbc_nc_user`` function of the ``features/environment.py`` module.

To run all tests that match *any* of a set of tags, separate the tags by commas.
For example, the following will run all of the *AR OP Consolidated HTML Email
Generation* (``generate-ar-op-cons-emails``) *AR OP Consolidated PDF Letter
Generation* (``generate-ar-op-cons-letters``) tests::

    $ behave --tags=generate-ar-op-cons-emails,generate-ar-op-cons-letters

To run all tests that match *all* of a set of tags, use separate ``--tags``
flags for each tag. For example, the following will run only the production
scenario of the *AR OP Consolidated HTML Email Generation* feature::

    $ behave --tags=generate-ar-op-cons-emails --tags=production

In addition to the general guidance just provided, all of the feature files in
the ``features/`` directory should contain comments clearly indicating how they
should be executed and whether they need any special configuration (flags).


Logging
--------------------------------------------------------------------------------

All log messages are written to a file named ``TSBC-NC-AUAT.log`` in the root
directory. Passing the ``--no-logcapture`` flag to ``behave`` will cause all of
the log messages to also be written to stdout.


Timeouts and attempt counters
--------------------------------------------------------------------------------

At various points, these tests wait for fixed periods of time or attempt to
perform some action a fixed number of times before giving up the attempt. The
variables holding these *wait* values are listed with their
defaults in `features/environment.py`_. If you find that tests are failing
because of timeouts being exceeded, or conversely that tests that should be
failing are waiting too long for an event that will never happen, you can
modify these *wait* values using behave user data flags, e.g.,
``-D pessimistic_wait=200``.


.. [1] The Gherkin syntax and the approach of defining features by describing
   user behaviours came out of the `behavior-driven development (BDD)`_
   process, which focuses on what a user wants a system to do, and not on how
   it does it. The `Behave documentation`_ provides a good overview of the key
   concepts and their origins in BDD.

.. _behave: https://github.com/behave/behave
.. _Gherkin: https://github.com/cucumber/cucumber/wiki/Gherkin
.. _Requests: http://docs.python-requests.org/en/master/
.. _nc: https://www.google.com/
.. _`Docker Compose`: https://www.google.com/
.. _`behavior-driven development (BDD)`: https://en.wikipedia.org/wiki/Behavior-driven_development
.. _`Behave documentation`: http://behave.readthedocs.io/en/latest/

