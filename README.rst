Software Patterns
#################

A Python package with common Software Design Patterns.


.. start-badges

.. list-table::
    :stub-columns: 1

    * - build
      - | |circleci| |codecov| |docs|

    * - package
      - | |pypi| |py_versions| |nb-pypi-downloads| |wheel| |commits_since|

    * - code quality
      - |better_code_hub| |scrutinizer|


|
| **Documentation:** https://software-patterns.readthedocs.io/en/master
| **Source Code:** https://github.com/boromir674/software-patterns/tree/master
| **CI/CD:** https://circleci.com/gh/boromir674/software-patterns/
|


Overview
========

This repository hosts the open-source code of the Software Patterns project.
The project's main component is the `software-patterns` python package hosted on Pypi at https://pypi.org/project/software-patterns
It also features online Documentation Pages hosted at https://software-patterns.readthedocs.io/ and
a public `CI workflow`_ hosted on CircleCI.


What are Software Design Patterns?

Software Engineers are employing various designs and solutions to solve their problems.
The emerging (software) patterns, among the code solutions, targeting reoccuring problems have been studied and
formalized in terms of how they are used, what problem they solve and why they are a fit candidate to solve it.
These code designs, which are frequently found in various code bases, are known as Software Design Patterns.


The `software-patterns` package exposes a set of Python Classes that allow convient usage of common
Software Design Patterns.


Design Patterns implemented:

* Notification (aka Broadcast/Listener pattern)
* Object Pool (aka Memoize)
* Classes Registry (aka Abstract Factory)
* Proxy


Installation
------------

Install from the Pypi server:

::

    pip install software-patterns

.. inclusion-marker-do-not-remove


Quickstart
----------


Example code to use the `factory` pattern in the form of a `(sub) class registry`:

.. code-block:: python

    from software_patterns import SubclassRegistry

    class MyClassRegistry(metaclass=SubclassRegistry):
        pass

    @MyClassRegistry.register_as_subclass('a')
    class ClassA:
        def __init__(self, number):
            self.attr = number

    @MyClassRegistry.register_as_subclass('b')
    class ClassB:
        def __init__(self, number):
            self.attr = number - 1

    assert MyClassRegistry.subclasses == {'a': ClassA, 'b': ClassB}

    instance_a = MyClassRegistry.create('a', 10)
    assert type(instance_a) == ClassA
    assert instance_a.attr == 10

    assert isinstance(instance_a, ClassA)

    instance_b = MyClassRegistry.create('b', 10)
    assert type(instance_b) == ClassB
    assert instance_b.attr == 9

    assert isinstance(instance_b, ClassB)




.. |circleci|  image:: https://img.shields.io/circleci/build/github/boromir674/software-patterns/master?logo=circleci
    :alt: CircleCI
    :target: https://circleci.com/gh/boromir674/software-patterns/tree/master


.. |codecov| image:: https://codecov.io/gh/boromir674/software-patterns/branch/master/graph/badge.svg?token=3POTVNU0L4
    :alt: Codecov
    :target: https://app.codecov.io/gh/boromir674/software-patterns/branch/master


.. |docs| image:: https://img.shields.io/readthedocs/software-patterns/master?logo=readthedocs
    :target: https://software-patterns.readthedocs.io/en/master/?badge=master
    :alt: Read the Docs (version)

.. |pypi| image:: https://img.shields.io/pypi/v/software-patterns?color=blue&label=pypi&logo=pypi&logoColor=%23849ed9
    :alt: PyPI
    :target: https://pypi.org/project/software-patterns/

.. |wheel| image:: https://img.shields.io/pypi/wheel/software-patterns?logo=python&logoColor=%23849ed9
    :alt: PyPI - Wheel
    :target: https://pypi.org/project/software-patterns

.. |py_versions| image:: https://img.shields.io/pypi/pyversions/software-patterns?color=blue&logo=python&logoColor=%23849ed9
    :alt: PyPI - Python Version
    :target: https://pypi.org/project/software-patterns

.. |commits_since| image:: https://img.shields.io/github/commits-since/boromir674/software-patterns/v2.0.0/master?color=blue&logo=Github
    :alt: GitHub commits since tagged version (branch)
    :target: https://github.com/boromir674/software-patterns/compare/v2.0.0..master



.. |better_code_hub| image:: https://bettercodehub.com/edge/badge/boromir674/software-patterns?branch=master
    :alt: Better Code Hub
    :target: https://bettercodehub.com/

.. |scrutinizer| image:: https://img.shields.io/scrutinizer/quality/g/boromir674/software-patterns/master?logo=scrutinizer-ci
    :alt: Scrutinizer code quality
    :target: https://scrutinizer-ci.com/g/boromir674/software-patterns/?branch=master

.. |nb-pypi-downloads| image:: https://img.shields.io/pypi/dm/software-patterns?logo=pypi&logoColor=%239AB3EE
    :alt: PyPI - Downloads


.. _`CI Workflow`: https://circleci.com/gh/boromir674/software-patterns
