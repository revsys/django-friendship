@_default:
    just --list

@bootstrap:
    python -m pip install --upgrade pip uv nox
    uv pip install --upgrade --requirement requirements.in

@fmt:
    just --fmt --unstable

@lint:
    python -m nox --reuse-existing-virtualenvs --session "lint"

@nox *ARGS:
    python -m nox --no-install --reuse-existing-virtualenvs {{ ARGS }}

@pip-compile:
    python -m uv pip compile --resolver=backtracking

@pre-commit:
    git ls-files -- . | xargs pre-commit run --config=.pre-commit-config.yaml --files

@test *ARGS:
    python -m nox --reuse-existing-virtualenvs \
        --session "test_django_version" \
        {{ ARGS }}

    python -m nox --reuse-existing-virtualenvs \
        --session "test_python_version" \
        {{ ARGS }}
