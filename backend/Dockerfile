
FROM docker.io/library/python:3.11-slim

# FIRST: Copy the db_config.cnf from the scope/ folder into the scope/backend/ folder.
COPY ./db_config.cnf /

ENV PYTHONUNBUFFERED=1

RUN groupadd app -g 1000 \
    && useradd -m -u 1000 -g app app \
    && apt-get update \
    && apt-get install -y --no-install-recommends python3-dev default-libmysqlclient-dev build-essential pkg-config \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get purge -y --auto-remove build-essential

WORKDIR /app
COPY . /app

RUN chown -R app:app /app

USER app

EXPOSE 8000

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
