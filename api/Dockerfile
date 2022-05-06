FROM python:3.9.5-slim-buster

WORKDIR /application

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

COPY requirements_dev.txt /application

RUN pip install -r requirements_dev.txt

COPY . /application