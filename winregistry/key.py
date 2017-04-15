import winreg
from datetime import datetime, timedelta

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
        keys_num, values_num, modify = winreg.QueryInfoKey(handle)
        resp['modify'] = datetime(1601, 1, 1) + timedelta(microseconds=modify/10)
    except:
        raise
    for key_i in range(0, keys_num):
        resp['keys'].append(winreg.EnumKey(handle, key_i))

    for key_i in range(0, values_num):
        value = {}
        value['value'], value['data'], value['type'] = winreg.EnumValue(handle, key_i)
        value['type'] = REG_TYPES[value['type']]
        resp['values'].append(value)

    handle.Close()
    reg.Close()

    return resp


def create(key, host=None, key_wow64_32key=False):
    ''' Delete named key from registry
    '''

    x64_key = winreg.KEY_WOW64_32KEY if key_wow64_32key else winreg.KEY_WOW64_64KEY
    access = winreg.KEY_WRITE | x64_key

    try:
        root, key_path = parse_path(key)
        parental, subkey = parse_subkey(key_path)

        reg = winreg.ConnectRegistry(host, root)
    except:
        raise

    handle = None
    is_exist = True
    subkeys = key_path.split('\\')
    current_path = ''
    i = 0

    while is_exist:
        try:
            handle = winreg.OpenKey(reg, current_path, 0, access)
            current_path = current_path + subkeys[i] + '\\'
            i += 1
        except FileNotFoundError:
            is_exist = False
            i = 0 if i == 0 else i - 1

    tail = '\\'.join(subkeys[i:])

    winreg.CreateKeyEx(handle, tail, 0, access)

    handle.Close()
    reg.Close()


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
