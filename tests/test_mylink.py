from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse
import unittest


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SITE_ROOT = REPOSITORY_ROOT / "MyLink"


class DocumentParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.anchors: list[dict[str, str]] = []
        self.local_assets: list[str] = []
        self.title_parts: list[str] = []
        self._inside_title = False

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        attributes = {name: value or "" for name, value in attrs}
        if tag == "a":
            self.anchors.append(attributes)
        elif tag == "link" and attributes.get("rel") == "stylesheet":
            self.local_assets.append(attributes.get("href", ""))
        elif tag in {"img", "script"}:
            self.local_assets.append(attributes.get("src", ""))

        if tag == "title":
            self._inside_title = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._inside_title = False

    def handle_data(self, data: str) -> None:
        if self._inside_title:
            self.title_parts.append(data)

    @property
    def title(self) -> str:
        return "".join(self.title_parts).strip()


class MyLinkPageTests(unittest.TestCase):
    def parse_index(self) -> DocumentParser:
        index_path = SITE_ROOT / "index.html"
        self.assertTrue(index_path.is_file(), "MyLink/index.html must exist")
        parser = DocumentParser()
        parser.feed(index_path.read_text(encoding="utf-8"))
        return parser

    def test_required_files_exist(self) -> None:
        required_paths = [
            SITE_ROOT / "index.html",
            SITE_ROOT / "styles.css",
            SITE_ROOT / ".nojekyll",
        ]

        for path in required_paths:
            with self.subTest(path=path.name):
                self.assertTrue(path.is_file(), f"required file is missing: {path}")

    def test_html_identity_and_https_links(self) -> None:
        parser = self.parse_index()

        self.assertEqual(parser.title, "MyLink")
        self.assertTrue(parser.anchors, "the page must expose at least one link")
        for anchor in parser.anchors:
            with self.subTest(href=anchor.get("href")):
                href = anchor.get("href", "")
                self.assertEqual(urlparse(href).scheme, "https")

    def test_local_assets_exist(self) -> None:
        parser = self.parse_index()

        self.assertIn("styles.css", parser.local_assets)
        for asset in parser.local_assets:
            with self.subTest(asset=asset):
                self.assertTrue(asset, "asset references must not be empty")
                self.assertFalse(urlparse(asset).scheme, "assets must remain local")
                self.assertTrue((SITE_ROOT / asset).is_file())

    def test_external_blank_links_are_hardened(self) -> None:
        parser = self.parse_index()

        blank_links = [
            anchor for anchor in parser.anchors if anchor.get("target") == "_blank"
        ]
        self.assertTrue(blank_links, "external links should open in a new tab")
        for anchor in blank_links:
            with self.subTest(href=anchor.get("href")):
                rel_values = set(anchor.get("rel", "").split())
                self.assertTrue({"noopener", "noreferrer"}.issubset(rel_values))


if __name__ == "__main__":
    unittest.main()
