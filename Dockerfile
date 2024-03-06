FROM python:3.12.2

# Python
ENV PYTHONUNBUFFERED=1 \
    # pip
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    \
    # Poetry
    # https://python-poetry.org/docs/configuration/#using-environment-variables
    POETRY_VERSION=1.6.1 \
    # make poetry install to this location
    POETRY_HOME="/opt/poetry" \
    # do not ask any interactive question
    POETRY_NO_INTERACTION=1 \
    # never create virtual environment automaticly, only use env prepared by us
    POETRY_VIRTUALENVS_CREATE=false

# prepend poetry to path
ENV PATH="$PATH:$POETRY_HOME/bin"

WORKDIR /project

RUN curl -sSL https://install.python-poetry.org | python3 -

COPY pyproject.toml /project/

# quicker install as runtime deps are already installed
RUN poetry cache clear --all .
RUN --mount=type=cache,target=/root/.cache \
    poetry install --no-root
