# Lego3
## Basic concepts
The test are run as follows:
```python -m pytest test.py```
Add optional `-s` flag to allow test to print to stdout
Add optional `-v` flag to make the test more verbose

In order to aquire a components use the `@pytest.mark.lego` decorator and pass it the wanted components. I.E.:
```
@pytest.mark.lego("8.8.8.8 or 8.8.6.6")
def test_dns(components):
    dns = components[0]
    assert "140.82.118.4"" == dns.get_ip("github.com")
```

The `@pytest.mark.lego` decorator communicates with the Lego manager.
Lego manager is central service which provides all the components.
It is run as follows:
```python lego_manager.py```

On the components SlaveServices are run as follows:
```python rpyc_classic.py --host 0.0.0.0```

## Lego manager responsibility
Contains the network's most updated structure.
The manager provides component to test by a query.
A query may result in none or many components.

## Development

Notice our [developer_guide](developer_guide.md) file for contributing the project.
