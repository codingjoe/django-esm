import warnings

import django.utils.deprecation
import pytest
from django.contrib.staticfiles.finders import get_finder
from django.core.checks import Error

from django_esm import storages


class TestESMFinder:
    finder = get_finder("django_esm.finders.ESMFinder")

    def test_find(self):
        assert self.finder.find("foo") == []
        assert (
            self.finder.find("testapp/static/js/index.js")
            == "testapp/static/js/index.js"
        )
        assert (
            self.finder.find("testapp/static/js/components/index.js")
            == "testapp/static/js/components/index.js"
        )
        assert self.finder.find("lit-html/lit-html.js", find_all=True) == []
        assert self.finder.find("foo/bar.js") == []

    @pytest.mark.skipif(
        not hasattr(django.utils.deprecation, "RemovedInDjango61Warning"),
        reason="Django < 5.2",
    )
    def test_find_with_deprecated_param(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = self.finder.find("testapp/static/js/index.js", all=True)
            assert len(w) == 1
            assert w[0].category == django.utils.deprecation.RemovedInDjango61Warning
            assert "deprecated in favor of" in str(w[0].message)
            assert result == ["testapp/static/js/index.js"]

    def test_list(self):
        all_files = self.finder.list([])
        assert ("testapp/static/js/index.js", storages.root_storage) in all_files
        assert (
            "testapp/static/js/components/index.js",
            storages.root_storage,
        ) in all_files

    def test_check(self, settings):
        assert not self.finder.check()

        settings.BASE_DIR = settings.BASE_DIR / "foo"

        assert self.finder.check() == [
            Error(
                "package.json not found",
                hint="Run `npm init` to create a package.json file.",
                obj=self.finder,
                id="django_esm.E001",
            )
        ]
