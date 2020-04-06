# Lego 3 - Developer Guide

This file has 2 main purposes:
1. Help you develop Lego 3 (core, libs or tests), avoid you from common mistakes and save your time when entering the project.
2. Keep Lego 3 repository clean and order, avoid conflicts between developers and save the time of who reads/uses your code. 

## Background

Lego 3 is a new distributed testing infrastructure used to test and monitor our products in the network.


## Required Knowledge

### Project

#### Requirements

*Optional*

Lego 3 is a completely new project, written from scratch, but its requirements based on insights from the previous testing infrastructure we used.

Read the requirements for this project [here](https://docs.google.com/document/d/1gSl9_jS_pIAkGtNLJSBKUGRbcOhALKMzv1ewWZSSElg/edit?usp=sharing) under "Requirments".

#### Terminology and Structure

*Mandatory*
 
Whether you already familiar with Lego or not, it is important to understand the new terminology of Lego 3 and its structure.

Read Lego 3 terminology [here](https://docs.google.com/document/d/1gSl9_jS_pIAkGtNLJSBKUGRbcOhALKMzv1ewWZSSElg/edit?usp=sharing) under "Terminology".

After understanding the new terms, have a look at the whole system structure [here](https://drive.google.com/file/d/1JM3AsNdA84BCSTigRS4oY59Pjh3VVl0Y/view?usp=sharing).


### Technology

#### Python 3.8

*Mandatory*

One of the requirements of this project is future proof.
The most updated Python version will help us ensure this.

Assuming advanced knowledge of Python 2, view [this](https://drive.google.com/drive/folders/1iZOsG1GowACO6pIsewtT3izaJmeAQGZN) lecture to notice the differences between Python 2 and Python 3.

#### PyTest

*Mandatory*

PyTest is a Python library used for testing.

Read [here](https://docs.pytest.org/en/latest/contents.html#toc) the following topics:
* Installation and Getting Started
* Usage and Invocations
* Using PyTest with an existing test suite
* The writing and reporting of assertions in tests
* PyTest fixtures: explicit, modular, scalable
* Marking test functions with attributes


#### RPyC

*Mandatory*

RPyC is a Python library for Python connection to remote devices.

It is one of the basic stones of Lego 3.

Read [here](https://rpyc.readthedocs.io/en/latest/index.html) the "Tutorial" and "Documentation" pharagraphes.

#### AsyncIO

*Optional*

AsycnIO is a built-in Python library enables asynchronous operations.

Lego 3 core is written especially to support the AsyncIO functionality.

Read [here](https://docs.python.org/3/library/asyncio.html) on the AsyncIO Python library.

## Lego 3 Repository

### Structrue

*Mandatory*

Lego 3 repository divided to the following directories:
* **docker**: All the docker files required to run a simulated Set-Up.
* **lego**: All the files related to lego plugin (i.e. lego core).
* **tests**: All the tests. In the future, the tests will locate in the product repositories in which they test.
* **components**: All the components in the network, including their RPyC connection and wrapped functionality.
* **libs**: User-defined libs that supply advanced functionality for components.
* **lego_manager**: The Lego main service responsible for resource allocation and test scheduling.

### Tests

*Mandatory*

Read both tests `test_tetanus.py` and `test_example.py`, make sure you understand everything!!

explanations:
* `@pytest.mark.lego` - This is a reference for lego plugin. What happens, in general, is that lego plugin request setup from the lego manager, and returns the requested components. Search for this decorator in `lego` dir to find its params docstrings.
* `def test(components)` - A fixture to return the requested components asked by the lego plugin.
* `async` or `asyncio.*` - Search in AsycnIO.
* `setup_method` or `setup_class` - Search in PyTest.

### Components

*Mandatory*

Read `zebra.py` and make sure you understand it.

### Libs

*Mandatory*

Read `tetanus.py` lib and make sure you understand it.

### Lego Manager

*Mandatory*

Read `lego_manager.py` and make sure you understand it.

### Lego Plugin

*Optional*

The plugin part is a little complicated and the development of the libs/tests doesn't demand the understanding of how the plugin works.

However, if you would like to go deeper into the project, you are more than invited to read `lego` directory files. [This](https://docs.pytest.org/en/latest/writing_plugins.html) can help you to understand the code there.

## Development Procedure

### Installation
#### Requirements

Before install and run the Lego project, make sure you have a Linux (recommended Ubunto) machine, with Python 3.8.2 installed.
 
#### Docker

The current project works with a Docker environment since we have no setup to model it.

To install Docker correctly, just follow [this link](https://docs.docker.com/install/linux/docker-ce/ubuntu/). 

#### Repository

Run the following commands:

```bash
sudo apt-get install resolvconf
git clone git@github.com:Steven17D/Lego3.git
cd Lego3/docker
docker-compose up --build
```

Notice you can monitor on the constraints by:
```bash
watch docker-compose ps
```

In another window (in Lego main path):
```bash
python3.8 -m pip install -e lego
python3.8 -m pytest tests/test_tetanus.py -v
```

All tests should pass successfully.

### Source and Tasks Control
#### Trello

Each Lego issue should be well documented in [Lego](https://trello.com/b/N1MDT9Lr/lego) Trello page.

How to contribute to Lego?

1. Select an issue to work on from the `to do` column.
2. Join your account to this issue.
3. Create a new branch in GitHub with the same name as the issue.
4. Join the branch to the issue using the GitHub extension.
5. Move the issue to the `WIP` column.
6. Develop a new feature (following the below instructions).
7. Open a PR in GitHub, and move the issue to `Review` column.
8. Repeat 7-8 phases until the PR approved.
9. Merge your branch and delete it.
10. Move the issue to the `Done` column. 

### Development
#### Pylint

Pylint is a Python static code analysis tool that looks for programming errors, helps to enforce a coding standard, sniffs for code smells and offers simple refactoring suggestions.

For keeping the code cleaner and understandable, before submitting you code make sure to pylint it as follow:

```bash
python3.8 -m pylint changed_dir/
```

#### Conventions

Before you start to develop any code, make sure you follow our [Python 3 conventions](https://docs.google.com/document/d/1wz1MVP0h7ZlklJ4UaLQiW4C15QLLoOj4x6NJKn_V0jA/edit?usp=sharing).


## Notes

### Merging issues

Any contibution of new code to `master` branch should pass the process of PR -> CR.
this is in purpose to keep the repository clean and order, and make sure the
contributed code doesn't harm any other code first, and second - do what it
suppose to do.

Up to now, the permission to merge to `master` can gave by one of us: Ariel Chinn,
Steven Dashevsky or Elyashiv Shayovitz.
