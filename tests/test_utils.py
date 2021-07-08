from winreg import KEY_READ, HKEY_LOCAL_MACHINE

from winregistry import WinRegistry
from winregistry.utils import (
    expand_short_root,
    get_access_key,
    parse_path,
)


def test_expand_short_root() -> None:
    root = expand_short_root("HKU")
    assert r"HKEY_USERS" == root, root


def test_expand_long_root() -> None:
    root = expand_short_root("SOME_LONG_STRING")
    assert "SOME_LONG_STRING" == root, root


def test_get_access_key() -> None:
    access_key = get_access_key(KEY_READ, True)
    assert access_key


def test_parse_path() -> None:
    path = r"HKLM\SOFTWARE\remove_me"
    root, path = parse_path(path)
    assert root == HKEY_LOCAL_MACHINE, root
    assert path == r"SOFTWARE\remove_me"


def test_get_key_handle() -> None:
    with WinRegistry() as reg:
        handler = reg.get_handler(
            r"HKLM\SOFTWARE",
            access=KEY_READ,
            key_wow64_32key=False,
        )
        assert handler


def test_read_entry() -> None:
    reg_key = r"HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion"
    with WinRegistry() as client:
        software_type = client.read_entry(reg_key, "SoftwareType")
    assert software_type.value == "System"


def test_write_entry() -> None:
    reg_key = r"HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion"
    with WinRegistry() as client:
        client.write_entry(reg_key, "remove_me", "test")
        test_entry = client.read_entry(reg_key, "remove_me")
        assert test_entry.value == "test"
        client.delete_entry(reg_key, "remove_me")


def test_delete_entry() -> None:
    reg_key = r"HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion"
    with WinRegistry() as client:
        client.write_entry(reg_key, "remove_me", "test")
        client.read_entry(reg_key, "remove_me")
        client.delete_entry(reg_key, "remove_me")
        try:
            client.read_entry(reg_key, "remove_me")
            raise AssertionError
        except FileNotFoundError:
            pass


def test_read_key() -> None:
    reg_key = r"HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion"
    with WinRegistry() as client:
        data = client.read_key(reg_key)
        assert data.entries
        assert data.reg_keys


def test_create_key() -> None:
    reg_key = r"HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\test\foo"
    with WinRegistry() as client:
        try:
            data = client.read_key(r"HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\test")
            raise AssertionError
        except FileNotFoundError:
            pass
        client.create_key(reg_key)
        data = client.read_key(r"HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\test")
        assert len(data.reg_keys) == 1, data
        assert "foo" in data.reg_keys, data
        client.delete_key(r"HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\test\foo")
        client.delete_key(r"HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\test")


def test_delete_key() -> None:
    reg_key = r"HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\test"
    with WinRegistry() as client:
        try:
            data = client.read_key(r"HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\test")
            raise AssertionError
        except FileNotFoundError:
            pass
        client.create_key(reg_key)
        client.delete_key(r"HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\test")
        try:
            data = client.read_key(r"HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\test")
            raise AssertionError
        except FileNotFoundError:
            pass
