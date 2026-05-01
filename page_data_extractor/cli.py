from __future__ import annotations

import argparse
from pathlib import Path
from urllib.request import urlopen

from page_data_extractor.extractor import extract_items, write_csv, write_json


def read_source(source: str) -> tuple[str, str]:
    if source.startswith(("http://", "https://")):
        with urlopen(source, timeout=20) as response:
            charset = response.headers.get_content_charset() or "utf-8"
            return response.read().decode(charset, errors="replace"), source
    return Path(source).read_text(encoding="utf-8"), ""


def build_base_url(source: str, explicit_base_url: str = "") -> str:
    if explicit_base_url:
        return explicit_base_url
    if source.startswith(("http://", "https://")):
        return source
    return ""


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract article-card data from an HTML page.")
    parser.add_argument("source", help="Local HTML file or http(s) URL.")
    parser.add_argument("--base-url", default="", help="Base URL for resolving relative links in local HTML files.")
    parser.add_argument("--json", dest="json_path", help="Output JSON path.")
    parser.add_argument("--csv", dest="csv_path", help="Output CSV path.")
    args = parser.parse_args()

    html, source_base_url = read_source(args.source)
    items = extract_items(html, base_url=build_base_url(args.source, args.base_url or source_base_url))

    if args.json_path:
        write_json(items, Path(args.json_path))
    if args.csv_path:
        write_csv(items, Path(args.csv_path))

    print(f"Extracted items: {len(items)}")
    for item in items:
        print(f"- {item['title']} | {item['url']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

