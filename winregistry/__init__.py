''' winregistry
    ~~~~~~~~~~~
    Minimalist `Python` library aimed at working with Windows registry.

    Usage::
        >>> from winregistry import WinRegistry as reg
        >>> path = 'HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run'
        >>> req = reg.write(path, 'notepad', 'notepad.exe')
        >>> req = reg.read(path, notepad)
        [('notepad', 'notepad.exe', 'REG_CZ')]
        >>> req = reg.delete(path, 'notepad')
'''
# from .key import Key as key
# from .value import Value as value
# from .utils import RegType as regtype


def write(key, value=None, data=None, regtype='REG_SZ', host=None, w64_k32=False):
    ''' Create new keys/values or stores data in the existing value field

        :param value_name: ...
        :param value: ...
        :param type:  ...
        :param host:  ...
        :param w64_k32:  ...
    '''
    pass

@staticmethod
def read(key, value=None, host=None, w64_k32=False):
    ''' Read values from registry keys

        :param value_name: ...
        :param host:  ...
        :param w64_k32:  ...
        :return: ...
        :rtype: ...
    '''
    pass
    # return ({'value': None, 'type': 'REG_SZ'})

@staticmethod
def remove(key, value=None, host=None, w64_k32=False):
    ''' Remove existing keys/values from registry

        :param value_name: ...
        :param host:  ...
        :param w64_k32:  ...
    '''
    pass
