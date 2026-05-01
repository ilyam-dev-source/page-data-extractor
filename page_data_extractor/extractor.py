from __future__ import annotations

import csv
import json
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable
from urllib.parse import urljoin


FIELDS = ("title", "url", "summary")


class CardParser(HTMLParser):
    def __init__(self, base_url: str = ""):
        super().__init__()
        self.base_url = base_url
        self.items: list[dict[str, str]] = []
        self._in_article = False
        self._current: dict[str, str] | None = None
        self._capture: str | None = None
        self._parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_dict = dict(attrs)
        if tag == "article":
            self._in_article = True
            self._current = {"title": "", "url": "", "summary": ""}
            return

        if not self._in_article or self._current is None:
            return

        if tag in {"h1", "h2", "h3"} and not self._current["title"]:
            self._start_capture("title")
        elif tag == "p" and not self._current["summary"]:
            self._start_capture("summary")
        elif tag == "a" and not self._current["url"]:
            href = attrs_dict.get("href")
            if href:
                self._current["url"] = urljoin(self.base_url, href)

    def handle_endtag(self, tag: str) -> None:
        if self._capture and tag in {"h1", "h2", "h3", "p"}:
            self._finish_capture()
            return

        if tag == "article" and self._current is not None:
            if self._current["title"] and self._current["url"]:
                self.items.append(self._current)
            self._current = None
            self._in_article = False

    def handle_data(self, data: str) -> None:
        if self._capture:
            self._parts.append(data)

    def _start_capture(self, field: str) -> None:
        self._capture = field
        self._parts = []

    def _finish_capture(self) -> None:
        if self._current is not None and self._capture is not None:
            text = normalize_text(" ".join(self._parts))
            self._current[self._capture] = text
        self._capture = None
        self._parts = []


def normalize_text(text: str) -> str:
    return " ".join(text.split())


def extract_items(html: str, base_url: str = "") -> list[dict[str, str]]:
    parser = CardParser(base_url=base_url)
    parser.feed(html)
    return parser.items


def write_json(items: Iterable[dict[str, str]], path: Path) -> None:
    path.write_text(json.dumps(list(items), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_csv(items: Iterable[dict[str, str]], path: Path) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        for item in items:
            writer.writerow({field: item.get(field, "") for field in FIELDS})

