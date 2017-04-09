# # edit key
# key_get(path)
# key_new(path)
# key_delete(path. incremental=False)
# key_rename(path, name)
# key_permissions
import winreg

from .utils import parse_path
from .utils import parse_subkey
from .utils import WINREG_TYPES as REG_TYPES


def read(key, host=None, key_wow64_32key=False):
    ''' Read data of a named key from registry
    '''

    resp = {'keys': [], 'values': []}

    x64_key = winreg.KEY_WOW64_32KEY if key_wow64_32key else winreg.KEY_WOW64_64KEY
    access = winreg.KEY_READ | x64_key

    try:
        root, key_path = parse_path(key)
        reg = winreg.ConnectRegistry(host, root)
        handle = winreg.OpenKey(reg, key_path, 0, access)

        resp['keys_num'], resp['values_num'], resp['modify'] = winreg.QueryInfoKey(handle)
    except:
        raise
    for key_i in range(0, resp['keys_num']):
        resp['keys'].append(winreg.EnumKey(handle, key_i))

    for key_i in range(0, resp['values_num']):
        value = {}
        value['value'], value['data'], value['type'] = winreg.EnumValue(handle, key_i)
        value['type'] = REG_TYPES[value['type']]
        resp['values'].append(value)

    handle.Close()
    reg.Close()

    return resp


def delete(key, host=None, key_wow64_32key=False):
    ''' Delete named key from registry
    '''

    x64_key = winreg.KEY_WOW64_32KEY if key_wow64_32key else winreg.KEY_WOW64_64KEY
    access = winreg.KEY_WRITE | x64_key

    try:
        root, key_path = parse_path(key)
        parental, subkey = parse_subkey(key_path)

        reg = winreg.ConnectRegistry(host, root)
        handle = winreg.OpenKey(reg, parental, 0, access)

        winreg.DeleteKey(handle, subkey)

        handle.Close()
        reg.Close()
    except:
        raise
