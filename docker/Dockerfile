FROM python:3.10-slim

# Define ARG with defaults at the top
ARG USER_NAME=ahmed
ARG USER_ID=1000
ARG HOME=/home/ahmed

ENV HOME=/home/ahmed \
    VIRTUAL_ENV=/home/ahmed/venv
ENV \
  PYTHONUNBUFFERED=1 \
  DEBIAN_FRONTEND=noninteractive \
  TZ=Europe/Warsaw \
  PATH="/usr/local/gcloud/google-cloud-sdk/bin:/home/ahmed/.local/bin:/home/ahmed/venv/bin:${PATH}" \
  PYTHONPATH="/app:${PYTHONPATH}" \
  BUILD_POETRY_LOCK="/home/ahmed/poetry.lock.build"

RUN apt-get -qq update \
    && apt-get -qq -y install vim gcc curl git build-essential libb64-dev \  
    && rm -rf /var/lib/apt/lists/* \
    && apt-get -qq -y clean

RUN curl https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-426.0.0-linux-x86_64.tar.gz > /tmp/google-cloud-sdk.tar.gz

RUN mkdir -p /usr/local/gcloud \
    && tar -C /usr/local/gcloud -xf /tmp/google-cloud-sdk.tar.gz \
    && /usr/local/gcloud/google-cloud-sdk/install.sh --usage-reporting false --command-completion true --bash-completion true --path-update true --quiet

# Create user with minimal options
RUN useradd -m -s /bin/bash ahmed

RUN chown -R ahmed:ahmed /home/ahmed

RUN mkdir -p /app && chown -R ahmed:ahmed /app /tmp

RUN curl -sSL https://install.python-poetry.org | python3 - --version 1.7.1

USER ahmed

COPY pyproject.toml *.lock /app/

WORKDIR /app

RUN poetry config virtualenvs.create false \
    && python3.10 -m venv /home/ahmed/venv \
    && pip install --upgrade pip setuptools \
    && poetry install && cp poetry.lock /home/ahmed/poetry.lock.build \
    && rm -rf /home/ahmed/.cache/*

USER root

COPY ./docker/scripts/* /

RUN chown -R ahmed /*.sh && chmod +x /*.sh

USER ahmed

COPY . /app/

RUN git config --global user.email "as4349124@gmail.com" \
    &&  git config --global user.name "Ahmed Sherif"

CMD ["/startup-script.sh"]