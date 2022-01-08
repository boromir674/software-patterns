Development
###########

In this section, we discuss several matters related to how development
is done through out the project.


Version Control
===============

For versioning our code we use git and github.com for hosting the open-source code in the web (online).

We use two long-living branches, `master` and `dev`.

Master branch
-------------

We use the `master` branch to tag "releases" published in github as well as
in pypi as python packages.

One should (only) branch of off master when there is the need to 'develop' a hotfix.
A hotfix is a topical branch that directly remedies a problem found in production code.
One example of such use case is when a bug is discovered that affects production code and the
need for fix rises immediately.


Dev Branch
----------

We use the 'dev' to facilitate development operations on the repository.

One should branch of off `dev` when developing for example a new feature, a ci improvement,
or a documentation addition/re-write.

Having a dedicated dev branch helps collaborators to rapidly acquire critical patches of code
despite working on separate branches. This is achieved with a sequence of merges, but more on this later.


Developer setup
===============

In order to do development on your local machine you should first get the code.
You should "clone" the code from github making sure you receive the dev branch
from the remote server.

Example command to clone code using ssh and checkout dev branch

    git clone git@github.com:boromir674/software-patterns.git --branch dev
    cd software-patterns

How to prepare your dev environment?
------------------------------------

Normally, a dev environment needs to facilitate some kind of write-code -> test-code loop.
In terms of python, that involves creating a 'virtual environment',
installing the package using the altered local source code, installing tooling (eg pytest) and running for example the test suite (unit tests).

However, in our development workflow there more activities involved than just running
our test suite in an (isolated) virtual environemnt.

A developer may also need to engage with activities such as build the documentation pages (eg into html),
generating visualizations of the codebase (ie generate *.svg files),
running a static code analyzer tool,
building the code into a wheel distribution, doing a code/package deployment, etc.

Most of the above activities/processes require some kind of python tool to be installed
in an separate isolated virtual environment and
subsequently invoked from a cli, with specific runtime arguments.

In order to automate running such python processes we use `tox` which manages
python environments using a declarating config file.

This way we roughly translate all the development activities into simple cli commands!

In the following sub sections you will find an illustration on how to run all the 
development processes in an automated way and how to run the 'local testing' process
in an alternative manual way.

Automated processes
*******************

To automate the various development processes we use the tox automation tool.
This allows us to map each process into a single cli command, as well as
use tox invokations as common front-end code between local and remote CI.

To use tox please install it with something like `pip install --user tox`
(its up to you to do a "global", "user" or in-a-virtual-environment' installation of tox).

    tox -av

Use tox -av for a complete enumeration and short description of all the tox environments that are available
to the developer out of the box. All these environemnts, dependencies, commands, environment variables, etc
can be found in file tox.ini.

tox --help is always available for an explanation of the cli parameters and flags.


** How to run local CI?

To run the default sequence of tox envs, (`mypy`, `clean` and `dev`) run:

tox

To run the test suite on the currently developed code (local git checkout) and measure code coverage run:

tox -e dev

To run mypy against the source code and do static type checking (similar to a compiled language), run:

tox -e mypy

To analyse the code and output information about errors, potential problems, convention violations and complexity you can run the prospector tool:

tox -e prospector

To generate local svg files depicting the dependency graphs, run:

tox -e graphs


Manually running tests
**********************

In this section, we present an alternative way to run the test suite against the developed
code. It is roughly equivalent to executing `tox -e dev` from the cli.

We first create a python `virtual environemnt`,
install the package in 'dev' mode (aka edit mode),
install a test-runner and then we are ready to do the
write-code -> test-code loop as many times as needed.

Sample environment setup, code and tooling installation commands:
   
    # Create a virtual environment in 'env-dev' directory
    pip install --user virtualenv && virtualenv env-dev --python=python3
    
    # Activate the virtual environment
    source env-dev/bin/Activate

    # Install the code in 'dev mode' (aka edit mode)
    pip install -e .

    # Install test-runner
    pip install pytest

The above commands should have set you up for starting to writing code.

Now you can loop the below steps as needed.

1. Change the code
2. Run test suite using test-runner with command `pytest tests -vv`


Contributing
============

*** How to branch?

Pick a short but descriptive name for your branch.

If developing a missing feature we recommend starting with a verb and using imperative.

Examples:

- for a feature to implement the Mediator pattern one might name their feature branch
as 'implement-mediator-pattern'
- for a feature to add a (class) factory method on the Observer class to facilitate
creating simple instances of the Observer class from runtime 'update callback' one
might name their branch as 'add-factory-method-in-observer'

Branch of off the dev branch.

git branch --track dev origin/dev
git checkout dev

For example, create topical branch as follows:

git checkout -b 'add-factory-method-in-observer' 


*** How to commit?

Of course if you make changes in the production code, make sure it is tested and fully covered
with unit tests.
Please strive for making atomic commits, meaning that each commit can act as
a stand-alone bulk of changes. Of course each bulk of changes should also be in
aggreement with the topic covered in the working branch.

In our opinion, atomic commits come with the following benefits:

- easier cherry-picking (less conflicts)
- easier merges (less conflicts)
- cleaner commits timeline visualizations


It is also a good idea to be consistent on how we format and write each commit's message.
To achieve that we use the 'commitizen' (cz) tool, which provides an interactive "commit message building" wizard through the cli.

Specifically, we use the so called cz-conventional-adapter, which defines commit messages semantics and format.

In practice, each time one is about to commit changes, they just needs to invoke `git cz` in place of `git commit`
and the wizard shall run on the terminal.

So, please install commitizen and the cz-conventional-adapter in your development environemnt.
A good starting point would be the script we provide that automatically installs commitizen in "user space"
and takes care of setting up the cz-conventional-adapter too.

You can read more about commitizen and the aforementioned cz-conventional-adapter [URLs].


*** How to do a pull-request?
A Pull Reqest can be opened either from a github cli or the gitub web interface.

We open a pull request whenever we are confident and want to signal that our branch has been developed to completion.
For any type of Pull Request we should adhere to the following principals:
- all commits are more or less atomic
    As discussed we promote the idea of having atomic commits on working branches
    That does not mean that the developer should refrain from committing as frequently as they want, since one can
    always do "commit squashing" before opening a pull request.

    git rebase dev --interactive

    At the end is does not matter how many commits end up in the branch, as long as they are atomic.


Feature Branches
----------------
All feature branches should be branched off of the 'dev' branch.
All Pull Requests should target the 'dev' branch.


For Feature Branch type of Pull Request we should adhere to the following principals:
-- all necessary business logic code is finished
-- all tests (old and new) are passing (both locally and in remote CI server)
-- all documentation sources have been updated
--- docstrings to build API ref in html
--- doctests written and passing
--- other documentation pages (eg section where we discuss what Software Desgin Patterns are included as modules in our package)
--- images embedded in docs pages that reflect the code architecture (dependency graphs and uml diagrams)

Apart from the above requirements we should pay attention to the evolution of the dev branch in the meantime.


If the dev branch has progressed from the commit that our branch's base started from, we need to make a decision.


Should our code immediately benefit from the changes incorporated in 'dev'?

If yes, then one has two options: to merge 'dev' into their branch or to rebase their branch on 'dev'

We recommend to merge the 'dev' code into our branch, because that way we clearly singal
what are the branch's topical commits and what are the merged changes. Importantly, this is evident on
the github web interface too, which is where peer-code-review, is done.

    git merge dev --no-ff

If no, then one can proceed with opening the Pull Request, which theoritically should still not produce any "conflicts",
assuming that each dev is commited to staying on-topic on their branch.


If dev branch has not progressed further from the commit where we intially based our branch off, we simply
proceed by opening a Pull Request (ie from the github web interface or cli).


Bugfixes (Hotfix Beanches)
--------------------------
All hotfix branches should be branched off of the 'master' branch.
All Pull Requests should target the 'master' branch.


For Bugfix (Hotfix) Branch type of Pull Request we should adhere to the following principals:

-- all necessary business logic fixes are finished
-- all tests (old and new) are passing (both locally and in remote CI server)
-- all documentation sources have been updated



*** How to run remote CI?


WE utilize a series of 3rd party web services to facilitate the various automated "actions" we undertake
during various stages of the development. 

CI/CD