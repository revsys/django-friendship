@_default:
    just --list

@fmt:
    just --fmt --unstable

@nox *ARGS:
    python -m nox --no-install --reuse-existing-virtualenvs {{ ARGS }}

@pip-compile:
    python -m piptools compile --resolver=backtracking

@pre-commit:
    git ls-files -- . | xargs pre-commit run --config=.pre-commit-config.yaml --files

@test *ARGS:
    python -m nox --reuse-existing-virtualenvs \
        --session "test_django_version" \
        --session "test_python_version" \
        {{ ARGS }}

lint:
    python -m nox --reuse-existing-virtualenvs --session "lint"
