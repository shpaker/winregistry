"""
# # edit value
# value_get(path, value)
# value_new(path, value)
# value_delete(path, value)
# value_rename(path, value, name)
# value_modify(path, value, data)
# value_modify_binary_data(path, value, data) """
import winreg
from winreg import KEY_WOW64_32KEY, KEY_WOW64_64KEY, KEY_READ, KEY_WRITE

from .utils import parse_path
from .utils import WINREG_TYPES


class Value(object):
    """ Object for working with registry keys
    """

    @staticmethod
    def read(path, computer=None, wow64_key32=False):
        """ Read a named value
        """
        x64_key = KEY_WOW64_32KEY if wow64_key32 else KEY_WOW64_64KEY
        access = KEY_READ | x64_key

        try:
            root, key_path, value_name = parse_path(path)
            reg = winreg.ConnectRegistry(computer, root)
            handle = winreg.OpenKey(reg, key_path, 0, access)
            value = winreg.QueryValueEx(handle, value_name)
            handle.Close()
        except:
            raise

        reg_type = WINREG_TYPES[value[1]]
        return {'value': value[0], 'type': reg_type}

    @staticmethod
    def write(path, value, reg_type='REG_SZ', computer=None, wow64_key32=False):
        """ Write (or create) a named value
        """
        x64_key = KEY_WOW64_32KEY if wow64_key32 else KEY_WOW64_64KEY
        root, key_path, value_name = parse_path(path)
        access = KEY_WRITE | x64_key

        try:
            winreg_type = getattr(winreg, reg_type)
            reg = winreg.ConnectRegistry(computer, root)
            handle = winreg.OpenKey(reg, key_path, 0, access)
            winreg.SetValueEx(handle, value_name, 0, winreg_type, value)
            handle.Close()
        except:
            raise

    @staticmethod
    def delete(path, computer=None, wow64_key32=False):
        """ Removes a named value from a registry key
        """
        x64_key = KEY_WOW64_32KEY if wow64_key32 else KEY_WOW64_64KEY
        access = KEY_WRITE | x64_key

        try:
            root, key_path, value_name = parse_path(path)
            reg = winreg.ConnectRegistry(computer, root)
            handle = winreg.OpenKey(reg, key_path, 0, access)
            winreg.DeleteValue(handle, value_name)
            handle.Close()
        except:
            raise
