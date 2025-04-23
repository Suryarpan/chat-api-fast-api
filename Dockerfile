FROM python:3.13-alpine

# Configure Poetry
ENV POETRY_VERSION=2.1.2
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv
ENV POETRY_CACHE_DIR=/opt/.cache

# Install poetry separated from system interpreter
RUN python3 -m venv $POETRY_VENV \
    && $POETRY_VENV/bin/pip install -U pip setuptools \
    && $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

# Add `poetry` to PATH
ENV PATH="${PATH}:${POETRY_VENV}/bin"

WORKDIR /app

COPY pyproject.toml poetry.lock poetry.toml README.md ./
RUN poetry install --no-interaction --no-cache --compile --no-root --no-directory --only main

COPY . .

RUN poetry install --only main

CMD [ "poetry", "run", "python", "-m", "chat_api.main" ]
