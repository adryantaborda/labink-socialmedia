FROM python:3.12-alpine

RUN apk udpate & \
    apk add bash nano

ENV PYTHONDOWNWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY ./requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 8000
