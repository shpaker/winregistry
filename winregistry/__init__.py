""" winregistry
    ~~~~~~~~~~~
    Minimalist Python library aimed at working with Windows registry.

    Usage::
        >>> import winregistry as reg
        >>> path = r'HKLM\SOFTWARE\remove_me'
        >>> reg.key.create(path + r'\test')
        >>> reg.value.write(path, 'Value name', 'Some data')
        >>> reg.key.read(path)
        {'keys': ['test'], 'values': [{'value': 'Value name', 'data': 'Some data', 'type': 'REG_SZ'}], 'keys_num': 1, 'values_num': 1, 'modify': 131367137267536662}
        >>> reg.value.read(path, 'Value name')
        {'value': 'Value name', 'data': 'Some data', 'type': 'REG_SZ', 'host': None}
        >>> reg.value.delete(path, 'Value name')
        >>> reg.key.delete(path + r'\test')
        >>> reg.key.read(path)
        {'keys': [], 'values': [], 'keys_num': 0, 'values_num': 0, 'modify': 131367138502814747}
        >>> reg.key.delete(path)
"""

from .key import read, create, delete
from .value import read, write, delete
