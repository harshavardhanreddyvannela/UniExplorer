# Backend (FastAPI)

Scaffold-only backend for UniExplorer.

## Planned API

- `GET /regions`
- `GET /regions/{region}/countries`
- `GET /regions/{region}/countries/{country}/universities`
- `GET /regions/north-america/us/{state}/universities`
- `GET /regions/north-america/canada/{province}/universities`
- `GET /search?name=...`

## Response Contract

- Endpoints return typed Pydantic response models from `backend/app/schemas.py`.
- University list responses currently return empty `items` placeholders until DB wiring is added.
- Shape consistency is enforced for:
  - region lists
  - country lists
  - country/state/province university lists
  - search results

## Run (after setup)

```bash
uvicorn backend.app.main:app --reload
```

## Lint and Format

```bash
ruff check backend
ruff format backend
cd frontend && npm run lint
```
