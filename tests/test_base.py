from django_esm.base import ServeESM
from django_esm.conf import get_settings


class _RecordingServeStatic:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs


class _StubServeESM(ServeESM, _RecordingServeStatic):
    pass


def test_defaults(settings):
    settings.DEBUG = True
    application = object()

    stub = _StubServeESM(application)

    assert stub.args == (application,)
    assert stub.kwargs == {
        "root": get_settings().STATIC_DIR,
        "prefix": get_settings().STATIC_PREFIX,
        "autorefresh": settings.DEBUG,
    }


def test_settings_override(settings, tmp_path):
    settings.ESM = {"STATIC_DIR": tmp_path / "modules", "STATIC_PREFIX": "modules"}

    stub = _StubServeESM("application")

    assert stub.kwargs["root"] == tmp_path / "modules"
    assert stub.kwargs["prefix"] == "modules"


def test_kwargs_override(settings, tmp_path):
    settings.ESM = {"STATIC_DIR": tmp_path / "modules", "STATIC_PREFIX": "modules"}

    stub = _StubServeESM(
        "application", root=tmp_path, prefix="overridden", autorefresh=False
    )

    assert stub.kwargs == {
        "root": tmp_path,
        "prefix": "overridden",
        "autorefresh": False,
    }


def test_autorefresh_follows_debug(settings):
    settings.DEBUG = False

    assert _StubServeESM("application").kwargs["autorefresh"] is False
