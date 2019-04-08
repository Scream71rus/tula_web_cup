FROM python:3.7.2-alpine3.8

RUN apk update && apk upgrade && \
    apk add --no-cache \
        gcc \
        git \
        postgresql-client \
        postgresql-dev \
        zlib-dev \
        libjpeg \
        tiff-dev \
        freetype-dev \
        lcms2-dev \
        libwebp \
        openjpeg-dev \
        tcl-dev \
        tk-dev \
        musl-dev \
        libmagic

RUN mkdir /home/application
RUN mkdir /home/application/filestore

COPY ./ /home/application/

WORKDIR /home/application/client

WORKDIR /home/application

RUN pip3 install -r requirements

RUN chmod +x ./docker-entrypoint.sh

ENV PGPASSWORD=twc

ENTRYPOINT ["/home/application/docker-entrypoint.sh"]
