Changelog
=========

1.1.0 (22-02-06)
-----------------

feature
^^^^^^^
- add apidoc & docs cmds to facilitate automatic docs generation & docs local build
- add memoize, notification, proxy & subclass registry software design patterns

test
^^^^
- cover all code with tests

documentation
^^^^^^^^^^^^^
- add url links to documentation, source code and ci/cd workflow
- clean readme
- update code comments
- add notes on what changes are included in the release in CHANGELOG.rst
- add developer guide & redesign chapters, sections, etc
- redesign documentation pages
- wip, dedicate a section for the patterns implementation in the documentation pages
- add docs landing page with logo & toc automatically generated with sphinx-apidoc tool
- fix doctests
- bump semantic version to 0.9.0

ci
^^
- rename job to a more intuitive name
- set the component depth to 3
- exclude 'docs' dir and all its contents from being analyzed
- exclude sphinx configuration python file from the 'production code'
- specify to treat *.py files in 'tests' dir as the 'test code'
- include only *.py files inside src/software_patterns dir as production code
- configure server to treat components starting at depth src/software_patterns/*
- configure sphinx to build the documentation files
- configure rtd to build docs with Sphinx and generate doc files in html, pdf & epub formats
- fix the installation command for job 'integration-test'
- add job to deploy package to test.pypi.org and job to install & test package after download
- fix ci workflow
- define jobs (ie build_n_test) and a workflow to run on CircleCI

1.0.0 (2022-01-10)
------------------

Changes
^^^^^^^

feature
"""""""
- include a developer guide in the documentation pages

developer
"""""""""
- add docs tox commands to facilitate automatic docs build locally

documentation
"""""""""""""
- add developer guide & redesign chapters, sections, etc
- dedicate a section for the patterns implementation in the documentation pages
- add landing page with logo

ci
""
- configure sphinx to build the documentation files
- use the readthedocs server to automatically build (generate html, pdf & epub files) and host the documentation pages



0.9.0 (2021-12-09)
------------------

Changes
^^^^^^^

feature
"""""""
- add memoize, notification, proxy & subclass registry software design patterns

ci
""
- define jobs (ie build_n_test) and a workflow to run on CircleCI
