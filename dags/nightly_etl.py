"""Nightly ETL: cron-driven, retries with backoff, secrets allowlist, asset outlet.

Graph edges come from passing task refs: ``clean = transform(rows)`` means
``transform`` needs ``extract``. At runtime each task runs as
``fn(secrets, envs)`` and reads upstream outputs via XCom / blob refs.
"""

from nozzle import Asset, task, workflow
from dags.utils.db import warehouse_dsn

orders = Asset("r2://warehouse/orders.parquet")


@workflow(schedule="0 3 * * *", retries=1)
def nightly_etl():
    @task(retries=3, secrets=["DB_PASS"], outlets=[orders])
    def extract(secrets, envs):
        assert secrets["DB_PASS"]
        assert envs["SINCE"]
        return {"watermark": envs["SINCE"], "rows": 12000}

    @task(retries=1)
    def transform(secrets, envs):
        return {"rows": 12000, "clean": True}

    @task
    def validate(secrets, envs):
        return {"ok": True}

    @task
    def load(secrets, envs):
        dsn = warehouse_dsn(envs)
        return {"loaded": 12000, "dsn": dsn}

    rows = extract()
    clean = transform(rows)
    checked = validate(clean)
    load(checked)
