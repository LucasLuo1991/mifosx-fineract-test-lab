# Project Overview

This repository is for practicing automation testing against a local Mifos/Fineract stack. The system under test includes:

- Mifos web app
- Fineract backend API
- PostgreSQL database
- ActiveMQ messaging service

The test suites use Python/pytest for database setup and verification, Postman/Newman for API testing, and Playwright with TypeScript for UI testing.

## Project Layout

- `mifosx-platform/` contains the Docker Compose setup for the local Mifos/Fineract environment. It is based on the PostgreSQL setup from [`openMF/mifosx-platform`](https://github.com/openMF/mifosx-platform/tree/main/postgresql).
- `mifosx-platform/docker-compose.yml` defines the web app, Fineract server, PostgreSQL, ActiveMQ, and optional Fineract worker services.
- `mifosx-platform/fineract-db/docker/` contains PostgreSQL environment values and the database initialization script.
- `database-setup/` contains Python dependencies and pytest-based database setup tests.
- `database-setup/tests/` contains Python tests that call Fineract APIs with `requests`, update sample test data, and verify PostgreSQL state with `SQLAlchemy`.
- `api-tests/` is for Postman collection JSON files used by Newman to test Fineract backend APIs.
- `ui-tests/` contains the Playwright test project, TypeScript configuration, and UI specs.
- `ui-tests/tests/` contains Playwright test files.

## Local Stack

Start the Mifos/Fineract stack from `mifosx-platform/`:

```powershell
docker compose up -d
```

Stop the stack from `mifosx-platform/`:

```powershell
docker compose down
```

By default, the checked-in environment maps services to these host URLs:

- Web app: `http://localhost:4200`
- Fineract API: `http://localhost:3000`
- PostgreSQL: `localhost:5432`

Check `mifosx-platform/fineract-db/docker/postgresql.env` before changing tests that depend on ports, credentials, tenant names, or database names.

## Test Commands

Install Python dependencies from `database-setup/`:

```powershell
python -m pip install -r requirements.txt
```

Run Python tests from `database-setup/`:

```powershell
python -m pytest
```

Install UI test dependencies from `ui-tests/`:

```powershell
npm install
```

Run Playwright tests from `ui-tests/`:

```powershell
npx playwright test
```

View the Playwright HTML report from `ui-tests/`:

```powershell
npx playwright show-report
```

Run Postman/Newman tests from `api-tests/` after collection files exist:

```powershell
newman run *-collection.json
```

## Coding Conventions

- Keep changes scoped to the relevant workspace: database setup, API tests, UI tests, or platform configuration.
- Use pytest conventions for Python tests.
- Use Playwright Test conventions for UI specs.
- Keep TypeScript Playwright tests in `ui-tests/tests/`.
- Keep Postman collections and Newman assets in `api-tests/`.
- Keep secrets, credentials, endpoints, and local overrides in ignored `.env`-style files when possible.
- Do not commit generated reports, caches, dependency folders, virtual environments, or local browser output.
- If adding `package.json` scripts, make them simple wrappers around the Playwright commands above.

## Verification

Before running test suites, make sure the Docker stack is running and healthy enough for the target suite.

When changing database setup or verification logic, run the relevant pytest command from `database-setup/`.

When changing API collections, run the relevant Newman command from `api-tests/`.

When changing Playwright tests or config, run the relevant `npx playwright test` command from `ui-tests/`. If browser binaries are missing, install them with Playwright before rerunning tests.

## Agent Notes

- Check the current working tree before editing and preserve user changes.
- Read nearby files before introducing new patterns.
- Prefer existing project structure over creating new top-level directories.
- Be careful with Docker volumes because they may contain local test data.
- Keep this file updated when new test workspaces, setup commands, required services, ports, or credentials are added.
