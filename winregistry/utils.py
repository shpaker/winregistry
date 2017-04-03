import winreg


def parse_path(path):
    try:
        _root, _path = path.split('\\', 1)
    except:
        raise

    if not _path:
        raise

    try:
        reg_root = getattr(winreg, _root.upper())
    except:
        raise

    try:
        key_path, value_name = _path.rsplit('\\', 1)
    except:
        raise

    if not value_name:
        raise KeyError('Key not found')

    return (reg_root, key_path, value_name)


def get_type(type):
    winreg_types = ['REG_NONE',              # 0 == winreg.REG_NONE
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

    return winreg_types[type]