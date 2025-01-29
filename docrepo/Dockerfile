# pull official base image
FROM python:3.12.5-alpine

# set work directory
WORKDIR /usr/src/docrepo

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

# install some diagnostics
RUN apk add nmap wget curl

# for transformations app
RUN apk add openjdk21
RUN apk add libreoffice
RUN apk add --no-cache msttcorefonts-installer fontconfig
RUN update-ms-fonts

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/docrepo/entrypoint.sh
RUN chmod +x /usr/src/docrepo/entrypoint.sh

# copy project
COPY apps ./apps
COPY config ./config
COPY mediafiles ./mediafiles
COPY staticfiles ./staticfiles
COPY extensions ./extensions
COPY .env ./.env
COPY manage.py ./manage.py

# run entrypoint.sh
ENTRYPOINT ["/usr/src/docrepo/entrypoint.sh"]
