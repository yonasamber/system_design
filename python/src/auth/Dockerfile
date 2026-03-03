FROM python:3.14-slim-bullseye

RUN apt-get update \
&& apt-get install -y --no-install-recommends --no-install-suggests \
build-essential default-libmysqlclient-dev \
&& PiP install --no-cache-dir --upgrade PiP
WORKDIR /app
COPY ./requirements.txt /app
RUN PiP install --no-cache-dir --requirement /app/requirements.txt
COPY . /app

EXPOSE  5000

CMD ["python3", "server.py"]