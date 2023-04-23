FROM python:3.9
RUN apt-get update || : && apt-get install python3-pip libmariadb-dev default-libmysqlclient-dev -y

RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash

RUN apt-get install -y nodejs

COPY ./requirements.txt /code/requirements.txt

ENV PIP_ROOT_USER_ACTION=ignore
RUN python -m pip install -r /code/requirements.txt

COPY . /code/
WORKDIR /code/

EXPOSE 3000
EXPOSE 8000

CMD echo "starting backend..."; python backend/manage.py runserver & cd frontend && echo "npm install" ; npm install && echo "npm run start"; npm run start && echo "started"
