********************************************************************************
  Developer Documentation (TSBC NC AUAT)
********************************************************************************

This document provides developer documentation for the TSBC NC Automated
User Acceptance Tests (TSBC NC AUAT). This is technical documentation for those
seeking to understand how these tests work and how to contribute to them.

The TSBC NC Automated User Acceptance Tests are high-level tests of the TSBC NC
APIs. The tests use Python Requests library to make requests to TSBC NC APIs.
They do some set-up, perform user actions, and make assertions about the
system's expected and desired behaviour. Behaviours are specified in
human-readable Gherkin *feature* files.

Gaining a thorough understanding of the tests requires understanding these three
layers:

1. `Feature files`_: these are human-readable test specifications (see
   `features/core/ <features/core/>`_).
2. `Step files`_: these are Python implementations of the steps used in the
   feature files (see `features/steps/ <features/steps/>`_).
3. The ``TSBCNCUser`` class in the `TSBC NC User package`_: this
   class has the ability to interact with TSBC NC APIs.

The following three sections describe each of these layers in more detail. The
`Configuration`_ section describes how arguments are passed to the ``behave``
CLI to configure how the tests are executed. Finally, the `Troubleshooting and
tips`_ section provides suggestions and help for writing and debugging features
and their implementations.


Feature files
================================================================================

What are feature files?
--------------------------------------------------------------------------------

Feature files describe features of the TSBC NC APIs.

    A feature is a unit of functionality of a software system that satisfies a
    requirement, represents a design decision, and provides a potential
    configuration option ([APEL-2009]_).

Each feature file defines a ``Feature`` by declaring one or more scenarios.
A ``Scenario`` represents a user performing a sequence of actions using one or
more TSBC NC APIs and expecting certain results. If a ``Scenario`` is a
``Scenario Outline``, then it will contain an ``Examples`` table and it will
run once for each configuration row in that table.

A scenario is constructed as a sequence of steps. Each step is a ``Given``, a
``When``, or a ``Then``. These setup preconditions, perform user actions, and
make assertions, respectively:

- ``Given``: put an API instance into a known state, e.g., upsert production
  templates.
- ``When``: perform a user action, e.g., generate and store a document using a
  particular template and test context.
- ``Then``: make an assertion about the state of an API, e.g., that a generated
  document is stored in the MDS and it has the expected properties.

The step lines of a feature file all begin with one of the following words:
``Given``, ``When``, ``Then``, ``And``, or ``But``. Steps beginning with
``And``, or ``But`` have the same meaning as the previous ``Given``, ``When``,
or ``Then``. For example, the following two scenarios are exactly equivalent::

    Given a DGS instance containing an up-to-date template <template_key>, including its template dependencies
    When a document of type <output_type> is generated from template <template_key> using data context <context_path>
    Then the generated document is stored in the MDS
    And the generated document is rendered correctly

    Given a DGS instance containing an up-to-date template <template_key>, including its template dependencies
    When a document of type <output_type> is generated from template <template_key> using data context <context_path>
    Then the generated document is stored in the MDS
    Then the generated document is rendered correctly

We allow for ``When+ Then+`` sequences to be repeated so that assertions may be
made between user actions. Thus the implicit grammar for a TSBC NC AUAT
scenario is::

    Given+ (When+ Then+)+

For more information on how to write Gherkin, see this Gherkin_ page and this
Behave_ page.


How to create new feature files
--------------------------------------------------------------------------------

New feature files should have the following properties.

1. **Names.** Feature file names have the ``.feature`` extension and are
   lowercase with hyphens used to separate words, e.g.,
   ``fpr-configuration.feature``.

2. **Location.** Feature files are stored in a subdirectory of the
   `features/ <features/>`_ directory, typically in
   `features/core/ <features/core/>`_.

   - Feature files in ``features/core/`` describe core features of
     the TSBC NC APIs; these features should run successfully against stable
     TSBC NC API releases.
   - Files that describe client or project-specific features may be placed in
     an appropriately named subdirectory of ``features/``, e.g.,
     ``features/CCA/``.

3. **Tags.** Tags are labels that can be applied to features and scenarios. They
   allow for the classification of features and scenarios. This classification
   allows users to control which features are executed when they run the
   ``behave`` command.

   - While they are technically optional from ``behave``'s point of view, each
     ``Feature`` in each feature file should contain a unique tag that
     succinctly identifies that feature, e.g., ``@generate-ar-op-cons-emails``,
     thereby allowing a user to run just that feature with ``behave
     --tags=generate-ar-op-cons-emails``.
   - Each ``Scenario`` or ``Scenario Outline`` should contain a descriptive tag
     that is at least unique within its ``Feature``, e.g., ``@production``;
     this allows a user to run just that scenario, e.g., with ``behave
     --tags=generate-ar-op-cons-emails --tags=production``.
   - Features and scenarios may contain more than one tag.
   - Tags are prefixed by the ``@`` character in feature files. When they are
     passed as arguments to ``behave``, the ``@`` character is optional, e.g.,
     ``--tags=wip`` and ``--tags=@wip`` are equivalent. Note that ``behave``
     tags are completely distinct from Python's decorator syntax, which is
     superficially similar in that it too uses the ``@`` character as a prefix.
   - The ``@wip`` and ``@non-executable`` tags have special meaning.

     - ``@wip`` is used to indicate a work-in-progress and signifies that
       the feature is not yet expected to execute successfully.
     - ``@non-executable`` is used to indicate that a feature or scenario is
       documentary in nature and should not be expected to execute successfully,
       i.e., pass.

4. **Syntax.** Feature files should be written following the formatting
   conventions exemplified in the extant feature files. Spaces, not tabs,
   should be used for indentation. Instead of providing a detailed
   specification, the following example of a truncated PID (Persistent
   Identifier) binding feature should suffice as a guide to formatting::

       @generate-ar-op-cons-emails
       Feature: AR OP Consolidated HTML Email Generation
         Clients of the TSBC NC APIs want to be able to generate HTML email documents
         using the Email Sending Service (ESS).

         @production
         Scenario Outline: Dan wants to generate the Accounts Receivable (AR) Operating Permit (OP) renewal HTML email documents using the DGS and confirm that the generated documents have the expected properties.
           Given a DGS instance containing an up-to-date template <template_key>, including its template dependencies
           When a document of type <output_type> is generated from template <template_key> using data context <context_path>
           Then the generated document is stored in the MDS
           And the generated document is rendered correctly

           Examples: templates and contexts
           | template_key                               | output_type | context_path                              |
           | ar_op_friendly_reminder_consolidated_email | text/html   | ar-op-friendly-reminder-consolidated.json |
           | ar_op_final_notice_consolidated_email      | text/html   | ar-op-final-notice-consolidated.json      |


5. **Documentation.** Comments in Gherkin feature files are lines of text preceded
   by the ``#`` character.

   - Each feature file should contain a comment indicating how it should be
     run, including any special arguments that must be passed to ``behave``.
     Best practice is to include a full ``behave`` command, including flags, as
     well as details of the type of TSBC NC deploy(s) that the behave
     command was successfully run against.

6. **Existing steps.** Whenever possible, new feature files should use existing
   step definitions. All existing steps are defined in Python modules under
   `features/steps/ <features/steps/>`_. To view a list of all existing
   steps, use ``behave`` to view the steps catalog::

       $ behave --steps-catalog


Step files
================================================================================

What are step files?
--------------------------------------------------------------------------------

Step files are Python modules defined under
`features/steps/ <_modules/features/steps/>`_. The steps used in scenarios are
implemented as step functions. For example, the following ``Given`` step may
appear in any scenario of any feature file::

    Given the default processing config is in its default state

and its implementation is provided by a particular Python function in
`features/steps/steps.py <features/steps/steps.py>`_::

    @given('the default processing config is in its default state')
    def step_impl(context):
        ...

A ``behave`` step function is a Python function named ``step_impl`` which is
decorated with one of ``@given``, ``@when``, and ``@then``. The decorator used
must match the initial keyword of the step. That is, a ``Given``-type step
needs a ``@given()``-decorated function, a ``When``-type step needs
``@when()``, and a ``Then``-type step needs ``@then()``.

The string argument passed to the decorator must *exactly* match the text of
the corresponding step (ignoring the ``Given/When/Then`` keyword), as
illustrated in the above two examples. The only exception to this is when the
argument contains variable patterns which are mapped to arguments passed to
``step_impl``. For example, the step::

    When a document of type text/html is generated from template ar_op_friendly_reminder_consolidated_email using data context ar-op-friendly-reminder-consolidated.json

is implemented by the following function::

    @when('a document of type {output_type} is generated from template'
          ' {template_key} using data context {context_path}')
    def step_impl(context, output_type, template_key, context_path):
        ...

where the parameter ``output_type`` will have value
``'text/html'``, ``template_key`` will have value
``'ar_op_friendly_reminder_consolidated_email'``, etc.

The ``context`` object is the first argument passed to every step function.
Behave supplies the context object as well as `several other objects`_ as
attributes of ``context``, e.g., ``context.feature`` and ``context.scenario``.
You can assign arbitrary values to any of these objects. The ``context`` object
persists across all features and scenarios that are run as a result of
executing the ``behave`` command. The ``context.feature`` object will be
re-initialized for each new feature that is run. Similarly, the
``context.scenario`` object will be re-initialized for each new scenario.

In order to preserve state across the steps within a given scenario, the step
functions of the TSBC NC AUAT tend to set attributes on the ``context.scenario``
object. For example, one step may download a generated document from the MDS
and save the file path as ``context.scenario.downloaded_file_path``. Then a
subsequent step can access the value of
``context.scenario.downloaded_file_path`` in order to validate the generated
file.


How to create new steps
--------------------------------------------------------------------------------

If you need to create a step in a feature file that is not yet implemented as a
step function, then you will need to define a decorated step function for it,
as described above.

The `features/steps/steps.py <features/steps/steps.py>`_ module is for
general-purpose steps. If a step is being used by more than one feature file,
it should be defined here. If this module becomes too large, it may be broken
up into multiple logically coherent modules.

Functions that do not implement steps (but which are called by step functions)
should be defined in `features/steps/utils.py <features/steps/utils.py>`_ and
imported into the step modules as needed.

Step implementations that are specific to a particular feature file should be
defined in a sensibly named module in `features/steps/ <features/steps/>`_.
For example, step functions particular to the
`generate-email-documents.feature <features/core/generate-email-documents.feature>`_
feature file are defined in
`features/steps/generate_email_documents_steps.py <features/steps/generate_email_documents_steps.py>`_.

In some cases, it is convenient to be able to execute one or more steps from
within a step. This can be done by calling the ``execute_steps`` method of the
``context`` object and passing in a string of step declarations using the same
syntax in the feature files. For example, the following in a step function::

    context.execute_steps(
        'Given the default processing config is in its default state\n'
        'And there is a standard GPG-encrypted space in the storage service')

would be equivalent to the following in a feature file scenario::

    Given the default processing config is in its default state
    And there is a standard GPG-encrypted space in the storage service

Remember to include the line breaks when calling ``execute_steps`` or it will
not work as expected.



TSBC NC User package
================================================================================

The TSBC NC User package in ``user/`` defines the ``TSBCNCUser``
class. An ``TSBCNCUser`` instance has "abilities" which allow it to
interact with TSBC NC APIs. For example, it might use its
``dgs`` ability to generate HTML or PDF documents using the Document Generator
Service (DGS).

The step functions described in the section above can access the
``TSBCNCUser`` instance using the ``tsbc_nc_user`` attribute of the
``context`` object. For example, in the step function for ``When a document of
type <output_type> is generated from template <template_key> using data context
<context_path>`` (in
`steps.py <features/steps/generate_email_documents_steps.py>`_) the document
is generated by using the TSBC NC User's DGS ability and calling
``context.tsbc_nc_user.dgs.generate_document(...)``.

The ``TSBCNCUser`` class and its abilities are structured using
composition and inheritance. The itemization below provides an overview of the
code structure as a guide for implementing new abilities or debugging existing
ones.

- `user/user.py <../user/user.py>`_: defines the ``TSBCNCUser``
  class (which inherits from `user/base.py::Base <../user/base.py>`_) with
  the following instance attributes representing abilities:

  - ``.dgs``: the DGS ability that uses the ``client.py`` module of the DGS
    source code to make API requests to a DGS deploy.

- `user/base.py <../user/base.py>`_: defines the ``Base`` class, which is a
  super-class of ``TSBCNCUser`` as well as of all of the ability
  classes, e.g., the ``DGSAPIAbility`` class that implements the
  DGS ability. The ``Base`` class does the following:

  - Initializes all of the URL getters as configured in
    `user/urls.py <../user/urls.py>`_.

- `user/utils.py <../user/utils.py>`_: contains general-purpose functions
  used by various TSBC NC User classes.

- `user/constants.py <../user/constants.py>`_: this module defines constants
  that are useful throughout the TSBC NC User package, e.g., default values
  like URLs or authentication strings, etc.


.. _configuration:

Configuration
================================================================================

The Python module `features/environment.py <features/environment.py>`_
defines a ``before_scenario`` function which is a hook that Behave_ calls
before each scenario is run. Each time this function is called, it instantiates
a new ``TSBCNCUser`` instance and passes in parameters to configure that
instance. These parameters are controlled by defaults, unless those defaults
are overridden by "behave userdata", i.e., command-line options of the form
``-D option-name=value``. For example, to configure the tests to target a
DGS instance at URL ``https://dgsapidev.technicalsafetybc.ca/api/`` and
authenticating with token ``<TOKEN>``::

    $ behave \
          -D dgs_url=https://dgsapidev.technicalsafetybc.ca/api/ \
          -D dgs_access_token=<TOKEN>


Troubleshooting and tips
================================================================================


How do I debug very long-running tests?
--------------------------------------------------------------------------------

Sometimes a test runs for several seconds getting an API into a certain state,
e.g., upserting particular templates, and performing user actions, e.g.,
downloading generated documents, before making any assertions. Then, if one of
those assertions fails because its code contains a bug, it would appear
necessary to run the entire test again in order to debug the new assertion
code. Often there is a simple strategy to avoid this.

1. First, comment out all steps prior to the assertion step in the feature
   file.
2. Then, modify the step function that implements the assertion so that it
   references the path to the downloaded/generated document from the original
   run of the test. Assuming the generated document was downloaded to
   ``.tsbc-nc-tmp/ar_op_final_notice_consolidated_email-1550082734.4325.html``,
   temporarily adding the following line to the beginning of the step function
   will usually suffice::

       context.scenario.downloaded_doc_path = '.tsbc-nc-tmp/ar_op_final_notice_consolidated_email-1550082734.4325.html'

3. Finally, re-running ``behave`` should result in just the assertion step
   running on the previously generated document.


How do I run the tests of the tests?
--------------------------------------------------------------------------------

The Python code in ``features/steps/`` and ``user/`` should adhere to `PEP
8`_. To test this locally, make sure you have tox_ and Pylint_ installed and
then call ``tox`` to run the tests on the tests::

    $ pip install -r requirements.txt
    $ tox


How long does it take to run the tests?
--------------------------------------------------------------------------------

The time required to run the TSBC NC API AUAT tests depends on how many and
which tests are being run, as well as the resources behind the TSBC NC API
instances being tested.


How are the tests run in practice?
--------------------------------------------------------------------------------

The TSBC NC tests have *not* yet been formally incorporated into Technical
Safety BC's manual or automated release processes.


.. _`PEP 8`: https://www.python.org/dev/peps/pep-0008/
.. _`tox`: https://tox.readthedocs.io/en/latest/
.. _`Pylint`: https://www.pylint.org/
.. _Behave: http://behave.readthedocs.io/en/latest/
.. _Gherkin: https://docs.cucumber.io/gherkin/
.. _Requests: http://docs.python-requests.org/en/master/
.. _`several other objects`: http://behave.readthedocs.io/en/latest/api.html#detecting-that-user-code-overwrites-behave-context-attributes

.. [APEL-2009] Sven Apel and Christian Kästner 2009. An Overview of Feature-Oriented Software Development (http://www.jot.fm/issues/issue_2009_07/column5/)

