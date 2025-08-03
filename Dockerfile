FROM python:3.13-bookworm

RUN apt-get -qq update && apt-get -qq --yes install curl vim netcat-openbsd

WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY app/bot /app/bot
COPY app/config /app/config
COPY app/main.py /app/main.py

CMD python /app/main.py
