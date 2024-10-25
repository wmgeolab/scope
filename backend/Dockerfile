
FROM docker.io/library/python:3.11-slim

WORKDIR /app
COPY . /app

# FIRST: Copy the db_config.cnf from the scope/ folder into the scope/backend/ folder.
COPY ./db_config.cnf /

ENV PYTHONUNBUFFERED=1

RUN groupadd app -g 1000 \
    && useradd -m -u 1000 -g app app \
    && apt-get update \
    && apt-get install -y --no-install-recommends default-libmysqlclient-dev build-essential \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get purge -y --auto-remove build-essential \
    && rm -rf /var/lib/apt/lists/* \
    && chown -R app:app /app

USER app

EXPOSE 8000

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
