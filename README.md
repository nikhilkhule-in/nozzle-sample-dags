# Nozzle sample DAGs

Public sample repo for the Cloudflare workflow orchestrator. DAGs are plain
Python using the `nozzle` SDK (`@workflow` / `@task` / `Asset`), schedules
live in the DAG files, and multi-module imports resolve from the repo root.

## Layout

- `dags/nightly_etl.py` — cron ETL with retries, secrets allowlist, asset outlet
- `dags/release.py` — manual-only release pipeline with independent branches
- `dags/utils/` — shared helpers imported by DAGs

## Conventions

- Task functions take `(secrets, envs)` bindings: `secrets["NAME"]` for
  ciphertext secrets, `envs["NAME"]` for plaintext vars.
- Return values chain tasks: `b = transform(a)` means `b` needs `a`.
- Large outputs should be written as blobs and passed by reference.

## Empty Commit
