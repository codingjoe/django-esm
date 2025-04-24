import pytest
from django.core.management import call_command
from django.core.management.base import SystemCheckError


def test_check_esm_settings(settings):
    settings.ESM = {}
    with pytest.raises(SystemCheckError):
        call_command("check")


def test_check_deployment(settings):
    settings.ESM = {}
    with pytest.raises(SystemCheckError):
        call_command("check", "--deploy")
