FROM python:3.9

ENV FLASK_APP app.py

ENV FLASK_ENV dev

WORKDIR app

COPY . /app

RUN pip install -r requirements_dev.txt

EXPOSE 5000

CMD python app.py
