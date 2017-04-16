winregistry
===========

.. image:: https://badge.fury.io/py/winregistry.svg
    :target: https://badge.fury.io/py/winregistry

.. image:: https://landscape.io/github/shpaker/winregistry/master/landscape.svg?style=flat
   :target: https://landscape.io/github/shpaker/winregistry/master
   :alt: Code Health

Minimalist Python library aimed at working with Windows Registry.

Installation
------------

.. code-block:: bash

    pip install winregistry

Usage
-----

.. code-block:: python

    >>> from winregistry import WinRegistry as Reg
    >>> reg = Reg()
    >>> path = r'HKLM\SOFTWARE\remove_me'
    >>> reg.create_key(path + r'\test')
    >>> True if 'remove_me' in reg.read_key(r'HKLM\SOFTWARE')['keys'] else False
    True
    >>> reg.write_value(path, 'Value name', b'21', 'REG_BINARY')
    >>> reg.read_key(path)
    {'keys': ['test'], 'values': [{'value': 'Value name', 'data': b'21...
    >>> reg.read_value(path, 'Value name')
    {'value': 'Value name', 'data': b'21', 'type': 'REG_BINARY'}
    >>> reg.delete_value(path, 'Value name')
    >>> reg.delete_key(path + r'\test')
    >>> reg.read_key(path)
    {'keys': [], 'values': [], 'modify': datetime.datetime(2017, 4, 16...
    >>> reg.delete_key(path)
    >>> True if 'remove_me' in reg.read_key(r'HKLM\SOFTWARE')['keys'] else False
    False

Usage with ``Robot Testing Framework`` Library
----------------------------------------------

.. code-block:: robotframework

    *** Settings ***
    Library    winregistry.robot

    *** Test Cases ***
    Valid Login
            ${path} =    Set Variable    HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run  
            Write Registry Value    ${path}             Notepad   notepad.exe                
            ${autorun} =            Read Registry Key   ${path}                              
            Delete Registry Value   ${path}             Notepad                              
