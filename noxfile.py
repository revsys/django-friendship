import nox

DJANGO_VERSIONS = ["4.2", "5.1", "5.2", "6.0", "6.1"]
PYTHON_VERSIONS = ["3.10", "3.11", "3.12", "3.13", "3.14", "3.14t", "3.15", "3.15t"]

# Django versions that have no final release yet need a specifier that opts in
# to pre-releases. Naming the pre-release also lets the same spec pick up the
# final release once it ships, so these entries can just be deleted then.
DJANGO_SPECS = {
    "6.1": "django>=6.1rc1,<6.2",
}

INVALID_PYTHON_DJANGO_SESSIONS = [
    ("3.10", "6.0"),
    ("3.11", "6.0"),
    ("3.10", "6.1"),
    ("3.11", "6.1"),
    ("3.14", "4.2"),
    ("3.14", "5.1"),
    ("3.14t", "4.2"),
    ("3.14t", "5.1"),
    # Django 4.2 and 5.1 are not compatible with Python 3.15 either
    ("3.15", "4.2"),
    ("3.15", "5.1"),
    ("3.15t", "4.2"),
    ("3.15t", "5.1"),
]

nox.options.default_venv_backend = "uv|venv"
nox.options.reuse_existing_virtualenvs = True


@nox.session(python=PYTHON_VERSIONS, tags=["django"], venv_backend="uv")
@nox.parametrize("django", DJANGO_VERSIONS)
def tests(session: nox.Session, django: str) -> None:
    if (session.python, django) in INVALID_PYTHON_DJANGO_SESSIONS:
        session.skip()
    # Editable so pytest collects ./friendship/tests rather than colliding with
    # a second copy installed into site-packages.
    session.install("-e", ".[test]")
    session.install(DJANGO_SPECS.get(django, f"django~={django}"))
    session.run("pytest", *session.posargs)


@nox.session(venv_backend="uv")
def lint(session: nox.Session) -> None:
    session.install(".[lint]")
    session.run("prek", "run", "--all-files", *session.posargs)


@nox.session(venv_backend="uv")
def docs(session: nox.Session) -> None:
    session.install(".[docs]")
    session.run("zensical", "build", *session.posargs)
    # Zensical has no plugin API yet, so generate llms.txt / llms-full.txt and
    # the per-page .md twins from the rendered site as a post-build step.
    session.run("python", "scripts/gen_llms.py", "site")


@nox.session(venv_backend="uv")
def coverage(session: nox.Session) -> None:
    # Editable, so coverage measures ./friendship rather than a copy in
    # site-packages that it would never see reported.
    session.install("-e", ".[test]", "django")
    session.run("pytest", "--cov", "--cov-report=term-missing", *session.posargs)


@nox.session(venv_backend="none")
def tests_env(session: nox.Session) -> None:
    """Run the tests in the active environment, without building a virtualenv."""
    session.run("pytest", *session.posargs)
