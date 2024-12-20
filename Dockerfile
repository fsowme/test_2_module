FROM python:3.11

RUN mkdir -p /data/app
RUN mkdir /data/clients

COPY requirements.txt /data/
RUN pip install -r /data/requirements.txt

COPY app /data/app
COPY clients /data/clients
COPY .env /data/

WORKDIR /data/app

CMD ["faust", "-A", "main", "worker", "-l", "info"]
