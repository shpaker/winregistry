from winreg import HKEY_CURRENT_USER, KEY_READ

from winregistry import WinRegistry
from winregistry._utils import expand_short_root, get_access_key, parse_path

TEST_REG_PATH = r"HKCU\SOFTWARE\_REMOVE_ME_"


def test_expand_short_root() -> None:
    root = expand_short_root("HKU")
    assert root == "HKEY_USERS", root


def test_expand_long_root() -> None:
    root = expand_short_root("SOME_LONG_STRING")
    assert root == "SOME_LONG_STRING", root


def test_get_access_key() -> None:
    access_key = get_access_key(KEY_READ, True)
    assert access_key


def test_parse_path() -> None:
    root, path = parse_path(TEST_REG_PATH)
    assert root == HKEY_CURRENT_USER, root
    assert path == TEST_REG_PATH.lstrip("HKCU\\")


def test_get_key_handle() -> None:
    with WinRegistry() as reg:

        handler = reg._get_handler(
            r"HKCU\SOFTWARE",
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
    with WinRegistry() as client:
        client.create_key(TEST_REG_PATH)
        client.write_entry(TEST_REG_PATH, "remove_me", "test")
        test_entry = client.read_entry(TEST_REG_PATH, "remove_me")
        assert test_entry.value == "test"
        client.delete_entry(TEST_REG_PATH, "remove_me")


def test_delete_entry() -> None:
    with WinRegistry() as client:
        client.create_key(TEST_REG_PATH)
        client.write_entry(TEST_REG_PATH, "remove_me", "test")
        client.read_entry(TEST_REG_PATH, "remove_me")
        client.delete_entry(TEST_REG_PATH, "remove_me")
        try:
            client.read_entry(TEST_REG_PATH, "remove_me")
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
    reg_key = r"HKCU\SOFTWARE\Microsoft\Windows NT\CurrentVersion\test\foo"
    with WinRegistry() as client:
        try:
            data = client.read_key(r"HKCU\SOFTWARE\Microsoft\Windows NT\CurrentVersion\test")
            raise AssertionError
        except FileNotFoundError:
            pass
        client.create_key(reg_key)
        data = client.read_key(r"HKCU\SOFTWARE\Microsoft\Windows NT\CurrentVersion\test")
        assert len(data.reg_keys) == 1, data
        assert "foo" in data.reg_keys, data
        client.delete_key(r"HKCU\SOFTWARE\Microsoft\Windows NT\CurrentVersion\test\foo")
        client.delete_key(r"HKCU\SOFTWARE\Microsoft\Windows NT\CurrentVersion\test")


def test_delete_key() -> None:
    reg_key = r"HKCU\SOFTWARE\Microsoft\Windows NT\CurrentVersion\test"
    with WinRegistry() as client:
        try:
            client.read_key(r"HKCU\SOFTWARE\Microsoft\Windows NT\CurrentVersion\test")
            raise AssertionError
        except FileNotFoundError:
            pass
        client.create_key(reg_key)
        client.delete_key(r"HKCU\SOFTWARE\Microsoft\Windows NT\CurrentVersion\test")
        try:
            client.read_key(r"HKCU\SOFTWARE\Microsoft\Windows NT\CurrentVersion\test")
            raise AssertionError
        except FileNotFoundError:
            pass


def test_delete_key_tree() -> None:
    reg_key = r"HKCU\SOFTWARE\Microsoft\Windows NT\CurrentVersion\test"
    with WinRegistry() as client:
        try:
            client.read_key(reg_key)
            raise AssertionError
        except FileNotFoundError:
            pass
        client.create_key(reg_key + "\\test1\\test3")
        client.write_entry(reg_key + "\\test1", "remove_me", "test")
        client.delete_key_tree(reg_key)
        try:
            client.read_key(reg_key)
            raise AssertionError
        except FileNotFoundError:
            pass


if __name__ == "__main__":
    for key, value in list(globals().items()):
        if callable(value) and key.startswith("test_"):
            print("Testing {0}".format(key))
            value()
