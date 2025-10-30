ARG PYTHON
FROM python:3.10

WORKDIR /jinja101
RUN useradd -m jinja101

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY --chown=jinja101:jinja101 . .

ENV UV_PROJECT_ENVIRONMENT=/usr/local
RUN uv sync --frozen --no-cache --all-extras

USER jinja101
RUN ansible-galaxy collection install ansible.netcommon

EXPOSE 5000/tcp

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "flask_app:app"]