FROM python:3.9.5-slim

RUN apt-get update -y
RUN apt-get -y install libpq-dev gcc

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV HBD_ENV=PRODUCTION
ENV DATABASE_URL postgres://application:1234@localhost/brewery

RUN mkdir /app
RUN mkdir /app/statics
WORKDIR /app
RUN pip install --upgrade pip
COPY . /app/
RUN pip install -r requirements.txt


CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]