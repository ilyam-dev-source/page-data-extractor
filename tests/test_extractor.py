import csv
import json
import tempfile
import unittest
from pathlib import Path

from page_data_extractor.extractor import extract_items, write_csv, write_json
from page_data_extractor.cli import build_base_url


SAMPLE_HTML = """
<html>
  <body>
    <article class="card">
      <h2>Junior Front End Developer</h2>
      <a href="/jobs/frontend">Apply</a>
      <p>Remote anywhere role.</p>
    </article>
    <article class="card">
      <h2>Web Scraping Expert</h2>
      <a href="https://example.com/scraping">Apply</a>
      <p>Extract and validate structured data.</p>
    </article>
  </body>
</html>
"""


class ExtractorTests(unittest.TestCase):
    def test_extract_items_from_article_cards(self):
        items = extract_items(SAMPLE_HTML, base_url="https://example.com")

        self.assertEqual(len(items), 2)
        self.assertEqual(items[0]["title"], "Junior Front End Developer")
        self.assertEqual(items[0]["url"], "https://example.com/jobs/frontend")
        self.assertEqual(items[0]["summary"], "Remote anywhere role.")
        self.assertEqual(items[1]["title"], "Web Scraping Expert")
        self.assertEqual(items[1]["url"], "https://example.com/scraping")

    def test_write_json_and_csv_outputs(self):
        items = extract_items(SAMPLE_HTML, base_url="https://example.com")

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            json_path = tmp_path / "items.json"
            csv_path = tmp_path / "items.csv"

            write_json(items, json_path)
            write_csv(items, csv_path)

            loaded_json = json.loads(json_path.read_text(encoding="utf-8"))
            self.assertEqual(loaded_json[1]["title"], "Web Scraping Expert")

            with csv_path.open("r", encoding="utf-8", newline="") as f:
                rows = list(csv.DictReader(f))
            self.assertEqual(rows[0]["url"], "https://example.com/jobs/frontend")
            self.assertEqual(rows[1]["summary"], "Extract and validate structured data.")

    def test_build_base_url_prefers_explicit_value_for_local_files(self):
        self.assertEqual(
            build_base_url("examples/sample_jobs.html", "https://example.com"),
            "https://example.com",
        )


if __name__ == "__main__":
    unittest.main()

