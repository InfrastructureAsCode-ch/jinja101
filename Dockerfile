ARG PYTHON
FROM python:3.8

WORKDIR /code
ENV PATH="/root/.poetry/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install curl -y \
    && rm -rf /var/lib/apt/lists/* \
    && curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python \
    && poetry config virtualenvs.create false

COPY pyproject.toml .
COPY poetry.lock .

RUN poetry install --no-dev --no-interaction --no-ansi

COPY . .

EXPOSE 5000/tcp

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "flask_app:app"]