# Scraper Template Contract

Create every geography scraper by copying `scrapers/template/scraper_template.py` and updating only the marked extension points.

## Required Output Schema

- `official_name` (required)
- `english_name` (optional)
- `region` (required)
- `country` (required)
- `website` (required)

## Pipeline Stages

1. fetch sources
2. parse to raw rows
3. normalize to contract
4. validate URLs and required fields
5. deduplicate by normalized domain
6. emit in-memory payload for DB write

## Error Policy

- Continue on row-level errors
- Print summary at end
- Never crash entire run for one bad row

## Retry Policy

- Attempts: `3`
- Delay: `1s`, `2s`, `4s`
- Timeout per request: `20s`
