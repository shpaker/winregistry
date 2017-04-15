""" 
     Class for working with Robot Testing Framework
"""
import winregistry.key as regkey
import winregistry.value as regvalue


class Keywords():

    @staticmethod
    def read_registry_key(key, host=None, key_wow64_32key=False):
        return regkey.read(key, host, key_wow64_32key)

    @staticmethod
    def create_registry_key(key, host=None, key_wow64_32key=False):
        regkey.create(key, host, key_wow64_32key)

    @staticmethod
    def delete_registry_key(key, host=None, key_wow64_32key=False):
        regkey.create(key, host, key_wow64_32key)

    @staticmethod
    def read_registry_value(key, value, host=None, key_wow64_32key=False):
        return regvalue.read(key, value, host, key_wow64_32key)

    @staticmethod
    def write_registry_value(key, value, data=None, reg_type='REG_SZ', computer=None, key_wow64_32key=False):
        regvalue.write(key, value, data, reg_type, computer, key_wow64_32key)

    @staticmethod
    def delete_registry_value(key, value, computer=None, key_wow64_32key=False):
        regvalue.delete(key, value, computer, key_wow64_32key)
