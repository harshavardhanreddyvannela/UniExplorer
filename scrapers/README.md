# Scrapers

This folder contains one placeholder scraper per geography unit.

## Uniform Contract

All scrapers follow `scrapers/template/scraper_template.py`.

## CLI (placeholder)

```bash
python -m scrapers.run --list
python -m scrapers.run --scraper regions.europe.germany
python -m scrapers.run --all
```

## Regenerate placeholders

```bash
zsh scripts/generate_scraper_placeholders.zsh
```

## Notes

- Country/state logic is intentionally not implemented yet.
- Placeholder files only define class naming and template inheritance.
- Runner now enforces exactly one concrete scraper class per module.
