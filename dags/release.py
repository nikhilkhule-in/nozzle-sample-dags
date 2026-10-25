"""Release pipeline: manual-only (no schedule), independent branches.

checkout fans out to build + docs; deploy waits on build only, so docs can
fail without blocking the release — failure stays local to its branch.
"""

from nozzle import task, workflow


@workflow()
def release():
    @task(retries=2)
    def checkout(secrets, envs):
        return {"sha": envs["GIT_SHA"]}

    @task(retries=1)
    def build(secrets, envs):
        return {"artifact": "api.tar.gz"}

    @task
    def docs(secrets, envs):
        return {"site": "docs/"}

    @task(retries=2)
    def deploy(secrets, envs):
        assert envs["TARGET"]
        return {"deployed": True}

    @task
    def notify(secrets, envs):
        return {"notified": True}

    src = checkout()
    pkg = build(src)
    pages = docs(src)
    live = deploy(pkg)
    notify(live)
    notify(pages)
