FROM nexus.halykbank.nb:9511/python:3.10.6-slim-buster

ENV TZ=Asia/Almaty
ENV PYTHONUNBUFFERED=1

WORKDIR /source

COPY requirements.txt ./

RUN pip install --no-cache-dir --proxy=$http_proxy --upgrade pip
RUN pip install --no-cache-dir --proxy=$http_proxy -r requirements.txt

COPY ./app ./app

CMD ["gunicorn", "-c", "app/gunicorn.conf.py", "app.main:init_app()"]
