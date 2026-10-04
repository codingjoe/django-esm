import pytest
from django.forms import Form
from django_esm import forms
from django_esm.exceptions import ModuleNotFound


class TestESM:
    def test_str(self, importmap_file):
        assert str(forms.ESM("local")) == (
            '<script type="module" src="/esm/local.js" integrity="sha256-local"></script>'
        )

        assert str(forms.ESM("remote")) == (
            '<script type="module" src="https://cdn.example.com/module.js"'
            ' integrity="sha256-remote"></script>'
        )

    def test_str__attributes(self, importmap_file):
        assert str(forms.ESM("local", nonce="s3cret")) == (
            '<script type="module" src="/esm/local.js" integrity="sha256-local"'
            ' nonce="s3cret"></script>'
        )

    def test_eq(self, importmap_file):
        """Avoid duplication and enable form media merging."""
        assert forms.ESM("local") == forms.ESM("local")

    def test_module_absent(self, importmap_file):
        with pytest.raises(ModuleNotFound, match="unknown"):
            forms.ESM("unknown")


class TestImportESModule:
    def test_deprecated(self, importmap_file):
        with pytest.warns(DeprecationWarning, match="use django_esm.forms.ESM"):
            asset = forms.ImportESModule("local")

        assert str(asset) == (
            '<script type="module" src="/esm/local.js" integrity="sha256-local"></script>'
        )


def test_media(importmap_file):
    class MyForm(Form):
        class Media:
            js = [forms.ESM("local")]

    assert str(MyForm().media) == (
        '<script type="module" src="/esm/local.js" integrity="sha256-local"></script>'
    )
