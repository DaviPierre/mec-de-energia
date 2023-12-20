FROM python:3.10.13

RUN apt-get update && \
    apt-get install -y libpq-dev

RUN useradd --create-home dev

WORKDIR /home/dev/mec-energia-api

USER dev

COPY . .

RUN pip install -U --no-cache-dir -r requirements.txt