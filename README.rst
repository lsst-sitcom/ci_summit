#########
ci_summit
#########


Description
===========

``ci_summit`` provides test scripts to run the Rubin Observatory
code on summit data.

Test Data
=========

``ci_summit`` requires the test data in the ``testdata_ci_summit``
package, which must be set up via eups first.

Running Tests
=============

To run this package locally:

- Clone this package and its dependencies. If you have setup ``lsst_sitcom``, you still need
  `ci_builder <https://github.com/lsst-dm/ci_builder>`_, and
  `testdata_ci_summit <https://github.com/lsst-sitcom/testdata_ci_summit>`_.
- ``setup -r ci_builder``
- ``cd ci_builder; scons; cd ..``
- ``setup -kr testdata_ci_summit``
- ``setup -kr ci_summit``
- From the root of this package directory run ``bin/rewrite.sh`` to rewrite python shebang lines.
- Run ``bin/ci_summit_run.py`` (see available options with ``--help``).

To cleanup after a run, use either ``bin/ci_summit_run.py --clean`` or ``rm -rf DATA/``.
