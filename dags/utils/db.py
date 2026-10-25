"""Shared helpers imported by DAGs (multi-module support)."""


def warehouse_dsn(envs) -> str:
    return f"warehouse://{envs['WAREHOUSE_HOST']}/analytics"


def blob_ref(run_id: str, name: str, size: int, sha256: str) -> dict:
    return {"blob": name, "size": size, "sha256": sha256, "run": run_id}
