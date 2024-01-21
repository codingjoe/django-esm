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
        assert self.finder.find("lit-html/lit-html.js", all=True) == [
            "lit-html/lit-html.js"
        ]
        assert self.finder.find("foo/bar.js") == []

    def test_list(self):
        all_files = self.finder.list([])
        assert ("testapp/static/js/index.js", storages.root_storage) in all_files
        assert (
            "testapp/static/js/components/index.js",
            storages.root_storage,
        ) in all_files
        assert ("lit-html/lit-html.js", storages.node_modules_storage) in all_files
        assert ("htmx.org/dist/htmx.min.js", storages.node_modules_storage) in all_files

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
