FROM python:3.12

ENV PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.8.2 \
    PATH="/root/.local/bin:$PATH" \
    PYTHONPATH=/src \
    TZ=Asia/Tokyo

WORKDIR /src

RUN pip install --upgrade pip && \
    curl -sSL https://install.python-poetry.org | python - --version $POETRY_VERSION && \
    poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock /src/

RUN poetry install
