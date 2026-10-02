import pytest
from django.core.management import call_command
from django.core.management.base import SystemCheckError
from django_esm.checks import check_deployment, check_esm_settings


def test_check_esm_settings(settings):
    settings.ESM = {"PACKAGE_DIR": ""}
    with pytest.raises(SystemCheckError):
        call_command("check")


def test_check_deployment(settings):
    settings.ESM = {"PACKAGE_DIR": ""}
    with pytest.raises(SystemCheckError):
        call_command("check", "--deploy")


def test_check_esm_settings__valid(settings, tmp_path):
    (tmp_path / "package.json").write_text("{}")
    (tmp_path / "importmap.json").write_text('{"imports": {}, "integrity": {}}')
    settings.ESM = {"PACKAGE_DIR": tmp_path, "STATIC_DIR": tmp_path}

    assert check_esm_settings(None) == []


def test_check_esm_settings__missing_static_dir(settings):
    settings.ESM = {"STATIC_DIR": ""}

    assert "esm.E003" in {error.id for error in check_esm_settings(None)}


def test_check_esm_settings__relative_static_dir(settings):
    settings.ESM = {"STATIC_DIR": "relative"}

    assert "esm.E004" in {error.id for error in check_esm_settings(None)}


def test_check_esm_settings__missing_static_prefix(settings):
    settings.ESM = {"STATIC_PREFIX": ""}

    assert "esm.E005" in {error.id for error in check_esm_settings(None)}


def test_check_esm_settings__missing_package_json(settings, tmp_path):
    settings.ESM = {"PACKAGE_DIR": tmp_path}

    assert "esm.E006" in {error.id for error in check_esm_settings(None)}


def test_check_esm_settings__missing_importmap(settings, tmp_path):
    settings.ESM = {"STATIC_DIR": tmp_path}

    assert "esm.W001" in {error.id for error in check_esm_settings(None)}


def test_check_deployment__missing_importmap(settings, tmp_path):
    settings.ESM = {"STATIC_DIR": tmp_path}

    assert [error.id for error in check_deployment(None)] == ["esm.E007"]
