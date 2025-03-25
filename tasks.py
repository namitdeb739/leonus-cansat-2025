# filepath: /Users/namitdeb/Developer/leonus-cansat-2025/tasks.py
from invoke import task, Context


@task
def activate(c: Context) -> None:
    c.run("source venv/bin/activate", pty=True)


@task
def deactivate(c: Context) -> None:
    c.run("deactivate", pty=True)


@task
def install(c: Context) -> None:
    c.run("pip install -r requirements.txt", pty=True)


@task
def run(c: Context) -> None:
    c.run("python main.py", pty=True)


@task
def test(c: Context) -> None:
    c.run("pytest", pty=True)


@task
def freeze(c: Context) -> None:
    c.run("pip freeze > requirements.txt", pty=True)


@task
def watch(c: Context) -> None:
    c.run("python watch.py", pty=True)


@task
def runlaptop(c: Context) -> None:
    c.run("python main.py laptop", pty=True)


@task
def runmonitor(c: Context) -> None:
    c.run("python main.py monitor", pty=True)


@task
def watchlaptop(c: Context) -> None:
    c.run("python watch.py laptop", pty=True)


@task
def watchmonitor(c: Context) -> None:
    c.run("python watch.py monitor", pty=True)


@task
def clearlogs(c: Context) -> None:
    c.run("rm -rf logs/*", pty=True)


@task
def makeplots(c: Context, csv: str) -> None:
    c.run(f"python plot_maker.py {csv}", pty=True)
