FROM docker.io/library/python:3.11-slim

COPY . /app
COPY ./db_config.cnf /
WORKDIR /app

ENV PYTHONUNBUFFERED=1

RUN groupadd app -g 1000 \
    && useradd -m -u 1000 -g app app \
    && apt-get update \
    && apt-get install -y default-libmysqlclient-dev build-essential \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get purge -y --auto-remove build-essential \
    && rm -Rf /var/lib/apt/lists/* \
    && chown -R app:app /app

USER app

CMD ["python3", "manage.py", "runserver"]