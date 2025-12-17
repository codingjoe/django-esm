from unittest.mock import Mock

import pytest
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
    try:
        import whitenoise  # noqa
    except ImportError:
        assert check_call.call_count == 1
    else:
        assert check_call.call_count == 2
    assert check_call.call_args_list[0][0][0] == [
        "npx",
        "--yes",
        "esimport",
        get_settings().PACKAGE_DIR,
        get_settings().STATIC_DIR,
    ]


def test_collectstatic__whitenoise(monkeypatch):
    pytest.importorskip("whitenoise")
    check_call = Mock()
    monkeypatch.setattr("subprocess.check_call", check_call)
    call_command("collectstatic", "--noinput")
    assert check_call.called
    assert check_call.call_count == 2
    assert check_call.call_args_list[0][0][0] == [
        "npx",
        "--yes",
        "esimport",
        get_settings().PACKAGE_DIR,
        get_settings().STATIC_DIR,
    ]
    assert check_call.call_args_list[1][0][0][1:] == [
        "-m",
        "whitenoise.compress",
        get_settings().STATIC_DIR,
    ]


def test_collectstatic__noesm(monkeypatch):
    check_call = Mock()
    monkeypatch.setattr("subprocess.check_call", check_call)
    call_command("collectstatic", "--noesm", "--noinput")
    assert not check_call.called
