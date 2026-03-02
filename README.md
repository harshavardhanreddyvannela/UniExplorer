# UniExplorer

Monorepo scaffold for:

- Next.js frontend (public directory)
- FastAPI backend (read-only public API)
- Python scraping pipeline (uniform per-geography scraper structure)

This scaffold intentionally avoids scraping logic and UI design implementation for now.

## Runtime Policy

- Dependency manifests are configured to pull latest stable versions at install time.
- Python packages in `requirements.txt` are intentionally unpinned.
- Frontend dependencies in `frontend/package.json` use `latest` tags.
- Version manager hints:
  - `.nvmrc` uses Node LTS track (`lts/*`)
  - `.python-version` uses current Python 3 line

## Linting Toolchain

- Python lint/format: Ruff (`ruff check .`, `ruff format .`)
- Frontend lint: OXC (`cd frontend && npm run lint`)

## Structure

- `frontend/` Next.js (App Router, SSG-ready route skeleton)
- `backend/` FastAPI + PostgreSQL contract skeleton
- `scrapers/` scraper template + geography placeholders
- `docs/` finalized scope decisions and conventions

## Key Decisions Applied

- Public directory only (no auth/admin for v1)
- Mandatory university fields: official name, region, country, website
- Optional: english name
- North America browse model includes US states + DC and Canada provinces/territories
- For North America university records, `country` stores first-level division name (example: `Texas`, `Ontario`)
- Sequential scraping; no async/rate-limit/proxy in v1
- Continue-on-error scraping with plain-text logging
- In-memory normalization pipeline, then database write (no raw snapshot persistence)

See `docs/specification.md` for full contract.

## Quick Setup

```bash
zsh scripts/bootstrap.sh
```

## Quality Commands

```bash
# Python
ruff check .
ruff format .

# Frontend
cd frontend && npm run lint
```
