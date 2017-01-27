FROM python:2.7.13-alpine
MAINTAINER knepperjm@gmail.com

COPY ./* /app/

RUN pip install requests && \
    chmod -R 755 /app

WORKDIR /app

CMD ["/bin/sh", "run.sh"]
