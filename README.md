# page-data-extractor

A small Python utility for extracting structured records from simple HTML job-card pages.

**Status: completed educational utility.**

## What it demonstrates

- Parsing HTML with the Python standard library.
- Extracting title, link, and summary fields.
- Normalizing text and resolving relative links against a base URL.
- Exporting structured data to JSON and CSV.
- Testing parser and output behavior with `unittest`.

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

## Scope

This compact utility is a support artifact for web data extraction and automation applications, rather than a production scraping system.
