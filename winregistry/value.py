''' Object for working with registry values
'''

import winreg
# from winreg import KEY_WOW64_32KEY, KEY_WOW64_64KEY, KEY_READ, KEY_WRITE

from .utils import parse_path
from .utils import WINREG_TYPES as REG_TYPES


def read(key, value, host=None, key_wow64_32key=False):
    ''' Read data of a named value from registry
    '''

    x64_key = winreg.KEY_WOW64_32KEY if key_wow64_32key else winreg.KEY_WOW64_64KEY
    access = winreg.KEY_READ | x64_key

    try:
        root, key_path = parse_path(key)
        reg = winreg.ConnectRegistry(host, root)
        handle = winreg.OpenKey(reg, key_path, 0, access)

        reg_value = winreg.QueryValueEx(handle, value)

        handle.Close()
        reg.Close()
    except:
        raise

    reg_type = REG_TYPES[reg_value[1]]

    data = {'value': value, 'data': reg_value[0], 'type': reg_type}
    data['host'] = host if host else None

    return data


def write(key, value, data=None, reg_type='REG_SZ', computer=None, key_wow64_32key=False):
    ''' Write (or create) a named value
    '''

    x64_key = winreg.KEY_WOW64_32KEY if key_wow64_32key else winreg.KEY_WOW64_64KEY
    access = winreg.KEY_SET_VALUE | x64_key

    try:
        root, key_path = parse_path(key)
        reg = winreg.ConnectRegistry(computer, root)
        handle = winreg.OpenKey(reg, key_path, 0, access)

        winreg.SetValueEx(handle, value, 0, getattr(winreg, reg_type), data)

        handle.Close()
        reg.Close()
    except:
        raise


def delete(key, value, computer=None, key_wow64_32key=False):
    ''' Removes a named value from a registry key
    '''
    x64_key = winreg.KEY_WOW64_32KEY if key_wow64_32key else winreg.KEY_WOW64_64KEY
    access = winreg.KEY_SET_VALUE | x64_key

    try:
        root, key_path = parse_path(key)
        reg = winreg.ConnectRegistry(computer, root)
        handle = winreg.OpenKey(reg, key_path, 0, access)

        winreg.DeleteValue(handle, value)

        handle.Close()
        reg.Close()
    except:
        raise

