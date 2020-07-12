# Background

Lego 3 is a new distributed testing infrastructure used to test and monitor our products in the network.

## Required Knowledge

### Project

#### Requirements (*Optional*)

Lego 3 is a completely new project, written from scratch, but its requirements based on insights from the previous testing infrastructure we used.

Read the requirements for this project [here](https://docs.google.com/document/d/1gSl9_jS_pIAkGtNLJSBKUGRbcOhALKMzv1ewWZSSElg/edit?usp=sharing) under "Requirements".

#### Terminology and Structure (*Mandatory*)

Whether you already familiar with Lego or not, it is important to understand the new terminology of Lego 3 and its structure.

Read Lego 3 terminology [here](https://docs.google.com/document/d/1gSl9_jS_pIAkGtNLJSBKUGRbcOhALKMzv1ewWZSSElg/edit?usp=sharing) under "Terminology".

After understanding the new terms, have a look at the whole system structure [here](https://drive.google.com/file/d/1JM3AsNdA84BCSTigRS4oY59Pjh3VVl0Y/view?usp=sharing).

### Technology

#### Python 3.8 (*Mandatory*)

One of the requirements of this project is future proof.
The most updated Python version will help us ensure this.

Assuming advanced knowledge of Python 2, view [this](https://drive.google.com/drive/folders/1iZOsG1GowACO6pIsewtT3izaJmeAQGZN?usp=sharing) lecture to notice the differences between Python 2 and Python 3.

#### PyTest (*Mandatory*)

PyTest is a Python library used for testing.

Read [here](https://docs.pytest.org/en/latest/contents.html#toc) the following topics:

* Installation and Getting Started
* Usage and Invocations
* Using PyTest with an existing test suite
* The writing and reporting of assertions in tests
* PyTest fixtures: explicit, modular, scalable
* Marking test functions with attributes

#### RPyC (*Mandatory*)

RPyC is a Python library for Python connection to remote devices.

It is one of the basic stones of Lego 3.

Read [here](https://rpyc.readthedocs.io/en/latest/index.html) the "Tutorial" and "Documentation" paragraphs.

#### AsyncIO (*Optional*)

AsycnIO is a built-in Python library enables asynchronous operations.

Lego 3 core is written especially to support the AsyncIO functionality.

Read [here](https://docs.python.org/3/library/asyncio.html) on the AsyncIO Python library.

## Lego 3 Repository

### Structure (*Mandatory*)

Lego 3 repository divided to the following directories:

* **docker**: All the docker files required to run a simulated Set-Up.
* **lego**: All the files related to lego plugin (i.e. lego core).
* **tests**: All the tests. In the future, the tests will locate in the product repositories in which they test.
* **components**: All the components in the network, including their RPyC connection and wrapped functionality.
* **libs**: User-defined libs that supply advanced functionality for components.
* **lego_manager**: The Lego main service responsible for resource allocation and test scheduling.

