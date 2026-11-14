from __future__ import annotations

import argparse
from html.parser import HTMLParser
from pathlib import Path
import sys
from urllib.parse import unquote, urlparse


class SiteDocumentParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.assets: list[str] = []
        self.links: list[dict[str, str]] = []

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        attributes = {name: value or "" for name, value in attrs}
        if tag == "a" and attributes.get("href"):
            self.links.append(attributes)
        elif tag == "link" and "stylesheet" in attributes.get("rel", "").split():
            self.assets.append(attributes.get("href", ""))
        elif tag in {"img", "script"}:
            self.assets.append(attributes.get("src", ""))


def verify_site(site_dir: Path) -> list[str]:
    site_root = site_dir.resolve()
    index_path = site_root / "index.html"
    if not index_path.is_file():
        return ["missing entry point: index.html"]

    parser = SiteDocumentParser()
    parser.feed(index_path.read_text(encoding="utf-8"))
    errors: list[str] = []

    for link in parser.links:
        href = link["href"]
        parsed = urlparse(href)
        scheme = parsed.scheme.lower()
        if parsed.netloc and not scheme:
            errors.append(f"external link must use https: {href}")
        elif scheme == "http":
            errors.append(f"external link must use https: {href}")
        elif scheme and scheme != "https":
            errors.append(f"unsupported link scheme: {href}")

        if link.get("target", "").lower() == "_blank":
            rel_values = {value.lower() for value in link.get("rel", "").split()}
            if not {"noopener", "noreferrer"}.issubset(rel_values):
                errors.append(
                    "target=_blank link must use rel=noopener noreferrer: " + href
                )

    for reference in parser.assets:
        parsed = urlparse(reference)
        if parsed.scheme or parsed.netloc:
            errors.append(f"asset must be local: {reference}")
            continue
        relative_path = unquote(parsed.path).lstrip("/")
        asset_path = (site_root / relative_path).resolve()
        try:
            asset_path.relative_to(site_root)
        except ValueError:
            errors.append(f"local asset escapes site root: {reference}")
            continue
        if not relative_path or not asset_path.is_file():
            errors.append(f"missing local asset: {reference}")

    return errors


def main(argv: list[str] | None = None) -> int:
    argument_parser = argparse.ArgumentParser(
        description="Validate a static site's entry point, assets, and links."
    )
    argument_parser.add_argument("site_dir", type=Path)
    arguments = argument_parser.parse_args(argv)

    errors = verify_site(arguments.site_dir)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"Verified static site: {arguments.site_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
