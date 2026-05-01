# page-data-extractor

Small Python portfolio project for extracting structured records from simple HTML job-card pages.

This project is intentionally small. It demonstrates:

- parsing HTML with the Python standard library;
- extracting title, link, and summary fields;
- normalizing text;
- resolving relative links against a base URL;
- exporting structured data to JSON and CSV;
- testing parser and output behavior with `unittest`.

It is not a production scraper and does not bypass access controls, paywalls, CAPTCHAs, or robots policies.

## Run tests

```powershell
python -m unittest discover -s tests
```

## Run on the sample file

```powershell
python -m page_data_extractor.cli examples\sample_jobs.html --base-url https://example.com --json out\items.json --csv out\items.csv
```

Create the `out` directory first if it does not exist.

## Why this exists

The project is meant as a more relevant support artifact for web scraping / data extraction freelance applications than a general C CLI project.

