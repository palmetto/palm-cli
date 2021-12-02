FROM python:{{python_version}}

COPY . /app/
WORKDIR /app
ENV PYTHONPATH=${PYTHONPATH}:${PWD}

RUN ./scripts/entrypoint.sh