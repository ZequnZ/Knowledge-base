FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --upgrade pip==20.2.4 \
    pip install --upgrade --upgrade-strategy=eager -r requirements.txt \
    pip install -U jupyterlab
