Common Lego3 Usage
=====================

Here you will see the common usage of Lego3.

Lego3.lego.pytest\_lego.plugin module
-------------------------------------

.. automodule:: Lego3.lego.pytest_lego.plugin

Components fixture
------------------

The components argument to test function is actually a pytest fixture with scope=function.
It means the component objects will be initialized before each test and closed after the test end.
Here is the docstring of components fixture (with an example for basic usage):

.. autofunction:: Lego3.lego.pytest_lego.plugin.components

Acquire setup
-------------
Here is the API lego manager exposes to outer service (and specifically to lego plugin) to get
the available component for the test's setup.

Lego3.lego\_manager.lego\_manager module
-------------------------------------------

.. automodule:: Lego3.lego_manager.lego_manager

LegoManager class
-------------------------------------------

.. autoclass:: Lego3.lego_manager.lego_manager.LegoManager
   :members: exposed_acquire_setup
