import winreg


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

SHORT_ROOTS = {
    'HKCR': 'HKEY_CLASSES_ROOT',
    'HKCU': 'HKEY_CURRENT_USER',
    'HKLM': 'HKEY_LOCAL_MACHINE',
    'HKU': 'HKEY_USERS',
    'HKCC': 'HKEY_CURRENT_CONFIG'}

def parse_path(path):
    try:
        _root, _path = path.split('\\', 1)
    except:
        raise

    if not _path:
        raise Exception()

    try:
        _root = _root.upper()
        _root = SHORT_ROOTS[_root] if _root in SHORT_ROOTS else _root
        reg_root = getattr(winreg, _root)
    except:
        raise

    try:
        key_path, value_name = _path.rsplit('\\', 1)
    except:
        raise

    if not value_name:
        raise KeyError('Key not found')

    return (reg_root, key_path, value_name)
