from django_esm import forms


class TestImportESModule:
    def test_str(self):
        assert str(forms.ImportESModule("@sentry/browser")) == (
            """<script type="module">import '@sentry/browser'</script>"""
        )

        assert str(forms.ImportESModule("#js/myEntryPoint")) == (
            """<script type="module">import '#js/myEntryPoint'</script>"""
        )

    def test_eq(self):
        """Avoid duplication and enable form media merging."""
        assert forms.ImportESModule("@sentry/browser") == forms.ImportESModule(
            "@sentry/browser"
        )
