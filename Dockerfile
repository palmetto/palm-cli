FROM python:3.8
COPY . /app
RUN export PYTHONPATH=/app
WORKDIR /app
RUN pip install -r dev-requirements.txt
