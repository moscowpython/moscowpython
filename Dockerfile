FROM python:3.11-slim as base

ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND=noninteractive

FROM base AS builder

RUN set -xe; \
    apt-get update && apt-get install -y \
        -o APT::Install-Recommends=false \
        -o APT::Install-Suggests=false \
            build-essential\
            gcc\
            g++ \
            libc-dev \
            libpq-dev \
            git \
            zlib1g-dev \
            curl \
            wget \
            ca-certificates \
            nodejs \
            npm

ADD requirements/base.txt /requirements.txt
RUN pip install --prefix=/install -r /requirements.txt


FROM node:12-alpine AS nodebuilder

COPY . /app
WORKDIR /app

RUN npm install
RUN npx gulp compile


FROM base

RUN groupadd --gid=800 -r unprivileged && useradd --uid=800 --gid=800 --no-log-init -r unprivileged

RUN set -xe; \
    apt-get update && apt-get install -y \
        -o APT::Install-Recommends=false \
        -o APT::Install-Suggests=false \
        locales \
        libpq-dev \
        tzdata

RUN dpkg-reconfigure -f noninteractive tzdata

COPY --from=builder /install /usr/local

COPY . /opt/app

COPY --from=nodebuilder /app/build /opt/app/moscowdjango/static

RUN chmod +x /opt/app/entrypoint.sh

WORKDIR /opt/app

RUN chown -R unprivileged:unprivileged /opt/app

RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

USER unprivileged

EXPOSE 8000

ENTRYPOINT ["/opt/app/entrypoint.sh"]
CMD ["runserver"]
