# Mifos/Fineract Test Workspace

This repository contains automation tests and local environment configuration for practicing against a local Mifos/Fineract stack.

The local stack includes:

- Mifos web app
- Fineract backend API
- PostgreSQL database
- ActiveMQ messaging service

Test coverage is split across Python/pytest database setup checks, Postman/Newman API collections, and Playwright UI tests.

Thanks to the Mifos and OpenMF projects for the upstream `mifosx-platform` work this local stack is based on, especially the PostgreSQL Docker Compose setup from `openMF/mifosx-platform`.

## Repository Layout

```text
.
+-- api-tests/          # Postman collections and Newman assets
+-- database-setup/    # Python pytest setup and database verification tests
+-- mifosx-platform/   # Docker Compose stack for Mifos/Fineract
`-- ui-tests/          # Playwright Test project
```

## Local Services

Start the stack from `mifosx-platform/`:

```powershell
docker compose --env-file ..\.env up -d
```

Stop the stack:

```powershell
docker compose down
```

Default host URLs:

| Service | URL |
| --- | --- |
| Web app | `http://localhost:4200` |
| Fineract server | `http://localhost:3000` |
| Fineract API base | `http://localhost:3000/fineract-provider/api` |
| Fineract health | `http://localhost:3000/fineract-provider/actuator/health` |
| PostgreSQL | `localhost:5432` |

Use the root `.env.example` as the template for local or Jenkins-specific values shared by Docker Compose, pytest, Playwright, and Newman. When starting Compose from `mifosx-platform/`, pass the root env file with `docker compose --env-file ..\.env up -d`.

The host-facing URLs default to the configured ports. Set `SERVER_URL`, `WEB_APP_URL`, `API_BASE_URL`, or `DB_ENDPOINT` only when a test needs a full URL/endpoint override.

`API_BASE_URL` is the base path without the version segment, for example `http://localhost:3000/fineract-provider/api`. Tests append `/v1` in their endpoint paths.

`WEB_APP_FINERACT_API_URL` is injected into the web app and is used by the browser. By default it is derived from `FINERACT_PORT`. Override it with `http://fineract-server:8080` when running Playwright inside the Compose `test-runner` container.

## Python Database Tests

Install dependencies from `database-setup/`:

```powershell
cd database-setup
python -m pip install -r requirements.txt
```

Run the pytest suite:

```powershell
python -m pytest
```

The tests read configuration from environment variables when present, otherwise they use local defaults:

| Variable | Default |
| --- | --- |
| `FINERACT_PORT` | `3000` |
| `WEB_APP_PORT` | `4200` |
| `POSTGRES_PORT` | `5432` |
| `SERVER_URL` | built from `FINERACT_PORT` |
| `WEB_APP_URL` | built from `WEB_APP_PORT` |
| `WEB_APP_FINERACT_API_URL` | built from `FINERACT_PORT` |
| `API_BASE_URL` | built from `SERVER_URL` as `/fineract-provider/api` |
| `API_USER` | `mifos` |
| `API_PASS` | `password` |
| `TENANT_ID` | `default` |
| `FINERACT_DB_USER` | `postgres` |
| `FINERACT_DB_PASS` | `your_secure_password_here` |
| `DB_ENDPOINT` | built from `POSTGRES_PORT` and `FINERACT_TENANT_DEFAULT_DB_NAME` |

## UI Tests

Install Playwright dependencies from `ui-tests/`:

```powershell
cd ui-tests
npm install
```

Run Playwright tests:

```powershell
npx playwright test
```

View the HTML report:

```powershell
npx playwright show-report
```

If browser binaries are missing, install them before rerunning tests:

```powershell
npx playwright install
```

## API Tests

Place Postman collection files in `api-tests/`. Once collections exist, run them with Newman from that directory:

```powershell
cd api-tests
newman run *-collection.json
```

## Development Notes

- Make sure the Docker stack is running before executing tests that call Fineract or PostgreSQL.
- Keep generated output out of source control, including caches, reports, dependency folders, virtual environments, and local browser artifacts.
- Keep workspace-specific changes inside the relevant directory: `database-setup/`, `api-tests/`, `ui-tests/`, or `mifosx-platform/`.
- Store local overrides and credentials in ignored `.env`-style files where possible.

## License and Attribution

This repository's original test workspace files are licensed under the license in `LICENSE`.

The `mifosx-platform/` Docker Compose workspace is based on upstream Mifos/OpenMF and Apache Fineract project material. Files derived from Apache-licensed upstream sources remain subject to the Apache License, Version 2.0, and their original license headers and notices should be kept intact when modified or redistributed. See the Apache License at <http://www.apache.org/licenses/LICENSE-2.0>.
