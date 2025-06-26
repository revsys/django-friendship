import nox

# DJANGO_STABLE_VERSION should be set to the latest Django LTS version
# and should *not* appear in DJANGO_VERSIONS

DJANGO_STABLE_VERSION = "5.2"
DJANGO_VERSIONS = ["4.2", "5.1", "5.2", "main"]

# PYTHON_STABLE_VERSION should be set to the latest stable Python version
# and should *not* appear in PYTHON_VERSIONS

PYTHON_STABLE_VERSION = "3.13"
PYTHON_VERSIONS = ["3.9", "3.10", "3.11", "3.12"]


INVALID_PYTHON_DJANGO_SESSIONS = [
    ("3.9", "5.1"),
    ("3.9", "5.2"),
]


nox.options.default_venv_backend = "uv|venv"
nox.options.reuse_existing_virtualenvs = True


@nox.session
def lint(session):
    session.install(".[lint]")
    session.run("python", "-m", "pre_commit", "run", "--all-files")


@nox.session(python=[PYTHON_STABLE_VERSION], tags=["django"])
@nox.parametrize("django", DJANGO_VERSIONS)
def test_django_version(session: nox.Session, django: str) -> None:
    if django == DJANGO_STABLE_VERSION:
        session.skip()

    session.install(".[test]")

    if django == "main":
        session.install("https://github.com/django/django/archive/refs/heads/main.zip")
    else:
        session.install(f"django~={django}.0")

    session.run("pytest", *session.posargs)


@nox.session(python=PYTHON_VERSIONS, tags=["python"])
@nox.parametrize("django", [DJANGO_STABLE_VERSION])
def test_python_version(session: nox.Session, django: str) -> None:
    if (session.python, django) in INVALID_PYTHON_DJANGO_SESSIONS:
        session.skip(
            f"Skipping invalid combination: Python {session.python} + Django {django}"
        )

    session.install(".[test]")
    session.install(f"django~={django}.0")
    session.run("pytest", *session.posargs)
