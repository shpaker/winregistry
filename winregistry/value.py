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


WINREG_TYPES = ['REG_NONE',              # 0 == winreg.REG_NONE
                'REG_SZ',                # 1 == winreg.REG_SZ
                'REG_EXPAND_SZ',         # 2 == winreg.REG_EXPAND_SZ
                'REG_BINARY',            # 3 == winreg.REG_BINARY
                'REG_DWORD',             # 4 == winreg.REG_DWORD
                # 4 == winreg.REG_DWORD_LITTLE_ENDIAN
                # 'REG_DWORD_LITTLE_ENDIAN',
                'REG_DWORD_BIG_ENDIAN',  # 5 == winreg.REG_DWORD_BIG_ENDIAN
                'REG_LINK',              # 6 == winreg.REG_LINK
                'REG_MULTI_SZ',          # 7 == winreg.REG_MULTI_SZ
                'REG_RESOURCE_LIST',     # 8 == winreg.REG_RESOURCE_LIST
                # 9 == winreg.REG_FULL_RESOURCE_DESCRIPTOR
                'REG_FULL_RESOURCE_DESCRIPTOR',
                # 10 == winreg.REG_RESOURCE_REQUIREMENTS_LIST:
                'REG_RESOURCE_REQUIREMENTS_LIST']


class Value(object):
    """ Object for working with registry keys
    """

    def __init__(self):
        pass

    @staticmethod
    def read(path, wow64_key32=False):
        x64_key = KEY_WOW64_32KEY if wow64_key32 else KEY_WOW64_64KEY
        root, key_path, value_name = parse_path(path)
        access = KEY_READ | x64_key

        try:
            handle = winreg.OpenKey(root, key_path, 0, access)
            value = winreg.QueryValueEx(handle, value_name)
            handle.Close()
        except:
            raise

        reg_type = WINREG_TYPES[value[1]]
        return {'value': value[0], 'type': reg_type}

    @staticmethod
    def write(path, value, reg_type='REG_SZ', wow64_key32=False):
        x64_key = KEY_WOW64_32KEY if wow64_key32 else KEY_WOW64_64KEY
        root, key_path, value_name = parse_path(path)
        access = KEY_WRITE | x64_key

        try:
            winreg_type = getattr(winreg, reg_type)
        except:
            raise

        try:
            handle = winreg.OpenKey(root, key_path, 0, access)
            winreg.SetValueEx(handle, value, 0, winreg_type, 2)
            handle.Close()
        except:
            raise

    def delete(self):
        pass

    def rename(self):
        pass
