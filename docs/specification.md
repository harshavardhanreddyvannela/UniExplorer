# UniExplorer v1 Specification (Scaffold)

## 1) Regions and Navigation

- Regions: `north-america`, `europe`, `asia-pacific`
- Frontend routes:
  - `/regions`
  - `/[region]/countries`
  - `/[region]/[country]`
  - North America only:
    - `/north-america/us/[state]`
    - `/north-america/canada/[province]`

`/[region]/countries` shows countries only.

## 2) Data Contract (University)

Mandatory:

- `official_name`
- `region` (`North America`, `Europe`, `Asia-Pacific`)
- `country`
- `website`

Optional:

- `english_name`

Not included in v1 table:

- `slug` (can be derived later if needed)

Normalization rules:

- Website canonicalization enforces `https` and uses final redirect target domain.
- Uniqueness key uses normalized domain.
- Name fields are UTF-8 and preserve diacritics.

Validation rule for accepting a row:

- URL syntax is valid
- Domain resolves
- HTTP response is success or redirect (`2xx` / `3xx`)

North America rule:

- `country` stores first-level division names for US/Canada (example: `Texas`, `Ontario`).

## 3) Scraper Contract

Each geography scraper follows the same high-level stages:

1. `fetch_sources()`
2. `parse_records()`
3. `normalize_records()`
4. `validate_records()`
5. `deduplicate_records()`
6. `emit_records()`

Execution model:

- Sequential
- Retry policy: 3 attempts, backoff `1s, 2s, 4s`
- Request timeout: `20s`
- Continue-on-error; collect failures and print summary

Input diversity:

- Website parsing, Excel ingestion, and API JSON are all supported, but implementation is per geography.

Output model:

- In-memory normalized rows are written to DB at the end of each scraper run.

## 4) Backend Contract

Stack:

- FastAPI
- PostgreSQL
- SQLAlchemy + Alembic

API v1:

- `GET /regions`
- `GET /regions/{region}/countries`
- `GET /regions/{region}/countries/{country}/universities`
- `GET /regions/north-america/us/{state}/universities`
- `GET /regions/north-america/canada/{province}/universities`
- `GET /search?name=...`

Search:

- PostgreSQL full-text index on `official_name` and `english_name`.

## 5) GraphQL Decision for v1

GraphQL is not included in initial scaffold to keep complexity low while taxonomy and scraping rules are still evolving.

Reasoning:

- REST endpoints already map cleanly to fixed navigation.
- No client-defined over-fetch/under-fetch requirement yet.
- Can be added later without breaking the scraping/backend core.

## 6) Asset Convention

- `public/regions/{region-slug}.svg`
- `public/flags/{country-code}.svg`
- `public/seals/{country-code}.svg` (country seal)

Standards:

- Country code: ISO-3166-1 alpha-2
- Region slugs: `north-america`, `europe`, `asia-pacific`

Fallback:

- Frontend must render safe placeholder when an SVG is missing.

## 7) i18n v1 Interpretation

v1 stores and serves:

- Native/official name
- Optional English name

UI language switching can be added later. For now, list rendering can choose one display mode and search against that same displayed field.

## 8) Dependency Version Policy

- Project installs target latest stable versions by default.
- Python dependencies are not version-pinned in `requirements.txt`.
- Frontend dependencies use `latest` tags in `frontend/package.json`.
- Node runtime follows `.nvmrc` (`lts/*`).
- Python runtime follows `.python-version` (`3`).
