import sys
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


def test_check_esm_settings__treeshake(monkeypatch):
    check_call = Mock()
    monkeypatch.setattr("subprocess.check_call", check_call)
    call_command("esm", "--treeshake")
    assert check_call.called
    assert check_call.call_count == 1
    assert check_call.call_args[0][0] == [
        "npx",
        "--yes",
        "esimport",
        get_settings().PACKAGE_DIR,
        get_settings().STATIC_DIR,
        "--treeshake",
    ]


def test_collectstatic(monkeypatch, capsys):
    check_call = Mock()
    monkeypatch.setattr("subprocess.check_call", check_call)
    call_command("collectstatic", "--noinput")
    assert check_call.call_count == 2
    assert check_call.call_args_list[0][0][0] == [
        "npx",
        "--yes",
        "esimport",
        get_settings().PACKAGE_DIR,
        get_settings().STATIC_DIR,
    ]
    assert check_call.call_args_list[1][0][0] == [
        sys.executable,
        "-m",
        "servestatic.compress",
        get_settings().STATIC_DIR,
    ]
    assert "ES modules compressed." in capsys.readouterr().out


def test_collectstatic__quiet(monkeypatch, capsys):
    check_call = Mock()
    monkeypatch.setattr("subprocess.check_call", check_call)
    call_command("collectstatic", "--noinput", verbosity=0)
    assert check_call.call_count == 2
    assert check_call.call_args_list[0][0][0][:3] == ["npx", "--yes", "esimport"]
    assert check_call.call_args_list[1][0][0] == [
        sys.executable,
        "-m",
        "servestatic.compress",
        get_settings().STATIC_DIR,
    ]
    assert "ES modules compressed." not in capsys.readouterr().out


def test_collectstatic__verbose(monkeypatch, capsys):
    check_call = Mock()
    monkeypatch.setattr("subprocess.check_call", check_call)
    call_command("collectstatic", "--noinput", verbosity=2)
    assert check_call.call_count == 2
    assert check_call.call_args_list[0][0][0][-1] == "--verbose"
    assert check_call.call_args_list[0][1]["stdout"] is sys.stdout
    assert check_call.call_args_list[1][1]["stdout"] is sys.stdout
    assert "ES modules compressed." in capsys.readouterr().out


def test_collectstatic__noesm(monkeypatch):
    check_call = Mock()
    monkeypatch.setattr("subprocess.check_call", check_call)
    call_command("collectstatic", "--noesm", "--noinput")
    assert not check_call.called


def test_collectstatic__treeshake(monkeypatch):
    check_call = Mock()
    monkeypatch.setattr("subprocess.check_call", check_call)
    call_command("collectstatic", "--noinput", "--treeshake")
    assert check_call.called
    assert check_call.call_args_list[0][0][0] == [
        "npx",
        "--yes",
        "esimport",
        get_settings().PACKAGE_DIR,
        get_settings().STATIC_DIR,
        "--treeshake",
    ]
