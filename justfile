@_default:
    just --list

@fmt:
    just --fmt --unstable

@nox *ARGS:
    nox --no-install --reuse-existing-virtualenvs {{ ARGS }}

@pip-compile:
    pip-compile --resolver=backtracking

@pre-commit:
    git ls-files -- . | xargs pre-commit run --config=.pre-commit-config.yaml --files

@test *ARGS:
    nox --reuse-existing-virtualenvs {{ ARGS }}
