winregistry
===========

Minimalist Python library aimed at working with Windows Registry.

Installation
------------

.. code-block:: bash

    pip install winregistry

Usage
-----

.. code-block:: python

    >>> import winregistry as reg
    >>> path = r'HKLM\SOFTWARE\remove_me'
    >>> reg.key.create(path + r'\test')
    >>> True if 'remove_me' in reg.key.read(r'HKLM\SOFTWARE')['keys'] else False
    True
    >>> reg.value.write(path, 'Value name', 'Some data')
    >>> reg.key.read(path)
    {'keys': ['test'], 'values': [{'value': 'Value name', 'data': 'Some data', 'type': 'REG_SZ'}], 'modify': datetime.datetime(2017, 4, 15, 7, 44, 15, 600890)}
    >>> reg.value.read(path, 'Value name')
    {'value': 'Value name', 'data': 'Some data', 'type': 'REG_SZ'}
    >>> reg.value.delete(path, 'Value name')
    >>> reg.key.delete(path + r'\test')
    >>> reg.key.read(path)
    {'keys': [], 'values': [], 'modify': datetime.datetime(2017, 4, 15, 7, 44, 50, 838510)}
    >>> reg.key.delete(path)
    >>> True if 'remove_me' in reg.key.read(r'HKLM\SOFTWARE')['keys'] else False
    False