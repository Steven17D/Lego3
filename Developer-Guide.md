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
### Tests
### Components
### Libs
### Lego Manager
### Lego Plugin

## Development Procedure

### Installation
#### Docker
#### Repository
#### Plugin

### Source and Tasks Control
#### Trello
#### GitHub

### Development
#### Lego 3 Tester
#### Debugging
#### Convensions

## Summary










Example:
link -  [pip](https://pip.pypa.io/en/stable/)
code - 
```bash
pip install foobar
```
