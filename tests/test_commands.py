from unittest.mock import Mock

from django.core.management import call_command

from django_esm.conf import get_settings


def test_check_esm_settings(monkeypatch):
    check_call = Mock()
    monkeypatch.setattr("subprocess.check_call", check_call)
    call_command("esm")
    assert check_call.called
    assert check_call.call_count == 1
    assert check_call.call_args[0][0] == [
        "npx",
        "--yes",
        "esimport",
        get_settings().PACKAGE_DIR,
        get_settings().STATIC_DIR,
    ]


def test_check_esm_settings__watch(monkeypatch):
    check_call = Mock()
    monkeypatch.setattr("subprocess.check_call", check_call)
    call_command("esm", "--watch")
    assert check_call.called
    assert check_call.call_count == 1
    assert check_call.call_args[0][0] == [
        "npx",
        "--yes",
        "esimport",
        get_settings().PACKAGE_DIR,
        get_settings().STATIC_DIR,
        "--watch",
    ]


def test_collectstatic(monkeypatch):
    check_call = Mock()
    monkeypatch.setattr("subprocess.check_call", check_call)
    call_command("collectstatic", "--noinput")
    assert check_call.called
    assert check_call.call_count == 1
    assert check_call.call_args[0][0] == [
        "npx",
        "--yes",
        "esimport",
        get_settings().PACKAGE_DIR,
        get_settings().STATIC_DIR,
    ]


def test_collectstatic__noesm(monkeypatch):
    check_call = Mock()
    monkeypatch.setattr("subprocess.check_call", check_call)
    call_command("collectstatic", "--noesm", "--noinput")
    assert not check_call.called
