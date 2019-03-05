FROM ubuntu:16.04

RUN apt-get update && apt-get install -y \
  software-properties-common \
  vim \
  && add-apt-repository ppa:jonathonf/python-3.6
RUN apt-get update -y
RUN apt-get install -y \
  build-essential \
  python3.6 \
  python3.6-dev \
  python3-pip \
  python3.6-venv

RUN python3.6 -m pip install pip --upgrade && \
  python3.6 -m pip install wheel

ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y \
  curl \
  alien \
  libaio1 \
  libaio-dev \
  libxrender1 \
  libfontconfig1 \
  rpm2cpio \
  cpio \
  unzip \
  mysql-client \
  libsasl2-dev \
  python-dev \
  libldap2-dev \
  libssl-dev \
  git \
  wget

ENV DEBIAN_FRONTEND noninteractive

ARG requirements_abs_path=/src/auat/requirements.txt

COPY requirements.txt /src/auat/requirements.txt
COPY requirements/ /src/auat/requirements/
RUN python3.6 -m venv /usr/lib/auatvenv
RUN /usr/lib/auatvenv/bin/pip install --upgrade pip
RUN /usr/lib/auatvenv/bin/pip install -r ${requirements_abs_path}

RUN set -ex \
    && groupadd --gid 333 --system auat \
    && useradd --uid 333 --gid 333 --system auat

ADD ./ /src/auat/
WORKDIR /src/auat

RUN set -ex \
    && mkdir /var/log/auat/ \
    && chown -R auat:auat /var/log/auat \
    && chown -R auat:auat /src/auat \
    && chown -R auat:auat /usr/lib/auatvenv

USER auat

ENTRYPOINT tail -f /dev/null
