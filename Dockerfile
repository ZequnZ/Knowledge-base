FROM python:3.9-slim

WORKDIR /app
# ARG PIP_EXTRA_INDEX_URL

RUN pip install -U jupyterlab