FROM python:3.9-alpine as base

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PIP_NO_CACHE_DIR false

RUN pip install --upgrade pip
RUN apk update && apk upgrade && \
    apk add --update --no-cache python3-dev gcc libc-dev libffi-dev

WORKDIR /app

COPY ./conf.py ./
COPY ./utils.py ./
COPY ./google_data_manager ./google_data_manager
COPY ./scrapers ./scrapers
COPY ./requirements.txt .

RUN pip install -r requirements.txt

FROM base as scheduling
COPY ./scheduling ./scheduling
CMD sh -c "python -m scheduling"
