# Lego3
## Basic consepts
The test are run as follows:
```python -m pytest test.py```
Add optinal `-s` flag to allow test to print to stdout

In order to aquire a slave use the `@get_slaves` decorator and pass it the wanted slaves. I.E.:
```
@get_slaves("8.8.8.8", "8.8.6.6")
def test_dns(slaves):
    for slave in slaves:
        assert "140.82.118.4"" == slave.get_ip("github.com")
```

The `@get_slaves` decorator communicates with the SlaveManager.
SlaveManager is central service which provides all the slaves for the aquired setup.
It is run as follows:
```python SlaveManager.py```

All slaves are SlaveServices. They are run as follows:
```python rpyc_classic.py```

## SlaveManager responsbilty
### Option A
Manages allocations.
And the SlaveManager creates the Lib instance and the connection to the slave.

Advatages:
* The test doesn't need to specify which Lib is needed. This is determined by the SlaveManager setup configuration.
* No need for the test to know the lib: This means that the test is very light
* All the slave connections are managed by the SlaveManager (not by the test itself)
* The setup configuration is stored in one place.

Disadvatages:
* All the traffic of all the running test must pass through the SlaveManager

### Option B
Manages allocations.

