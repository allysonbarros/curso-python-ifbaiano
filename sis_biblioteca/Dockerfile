FROM python:2-stretch
ENV PYTHONUNBUFFERED 1

ENV APP_USER app
ENV APP_ROOT /app

WORKDIR ${APP_ROOT}
ADD requirements.txt ${APP_ROOT}
RUN pip install -r requirements.txt

RUN adduser --disabled-password --gecos '' ${APP_USER}
ADD . ${APP_ROOT}