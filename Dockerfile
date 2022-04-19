FROM python:3.8-alpine

ENV FLASK_APP = app
ENV FLASK_ENV = production

WORKDIR APP

COPY . /APP

CMD ['pip', 'install', '-r', 'requirements.txt']

RUN flask run
