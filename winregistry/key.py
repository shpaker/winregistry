# # edit key
# key_get(path)
# key_new(path)
# key_delete(path. incremental=False)
# key_rename(path, name)
# key_permissions
import winreg


class Key(object):
    """ Object for working with registry keys
    """

    def __init__(self):
        pass

    @staticmethod
    def read_values(self):
        pass

    @staticmethod
    def read_keys():
        pass

    def create(self):
        pass

    def delete(self):
        pass

    def rename(self):
        pass
