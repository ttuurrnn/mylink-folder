from importlib import import_module
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest


class VerifySiteTests(unittest.TestCase):
    def load_verifier(self):
        try:
            module = import_module("scripts.verify_site")
        except ModuleNotFoundError:
            self.fail("scripts.verify_site must exist")
        return module.verify_site

    def create_site(self, index_html: str, assets: tuple[str, ...] = ()) -> Path:
        temporary_directory = TemporaryDirectory()
        self.addCleanup(temporary_directory.cleanup)
        site_root = Path(temporary_directory.name)
        (site_root / "index.html").write_text(index_html, encoding="utf-8")
        for asset in assets:
            asset_path = site_root / asset
            asset_path.parent.mkdir(parents=True, exist_ok=True)
            asset_path.write_text("/* fixture */", encoding="utf-8")
        return site_root

    def test_valid_site_has_no_errors(self) -> None:
        site_root = self.create_site(
            """<!doctype html>
            <html><head><link rel="stylesheet" href="styles.css"></head>
            <body><a href="https://example.com" target="_blank"
            rel="noopener noreferrer">Example</a></body></html>""",
            assets=("styles.css",),
        )

        errors = self.load_verifier()(site_root)

        self.assertEqual(errors, [])

    def test_missing_local_asset_is_reported(self) -> None:
        site_root = self.create_site(
            """<!doctype html>
            <html><head><link rel="stylesheet" href="missing.css"></head>
            <body></body></html>"""
        )

        errors = self.load_verifier()(site_root)

        self.assertIn("missing local asset: missing.css", errors)

    def test_insecure_external_link_is_reported(self) -> None:
        site_root = self.create_site(
            """<!doctype html>
            <html><head></head><body>
            <a href="http://example.com">Example</a>
            </body></html>"""
        )

        errors = self.load_verifier()(site_root)

        self.assertIn("external link must use https: http://example.com", errors)


if __name__ == "__main__":
    unittest.main()
