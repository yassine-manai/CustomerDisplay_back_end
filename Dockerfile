FROM python:3.12-slim


WORKDIR /app
COPY . /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /app/requirements.txt

# tzdata for timzone
RUN apt-get update -y
RUN apt-get install -y tzdata
 
# timezone env with default
ENV TZ=UTC

ENV APP_IP=127.0.0.1
ENV APP_PORT=8200

ENV SERVER_IP=demo.asteroidea.co
ENV SERVER_PORT=8092

ENV POS_IP=192.168.1.7
ENV POS_PORT=8000
ENV POS_API=/local/pos_config

ENV CRON=1

CMD ["python3", "/app/main.py"]
#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]