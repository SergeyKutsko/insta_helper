FROM python:3.10
USER root
RUN mkdir -p /app
WORKDIR /instagram
COPY instagram/requirements.txt .
RUN apt-get update && apt-get install -y sudo
RUN apt-get install gettext -y
RUN pip install -r requirements.txt

COPY instagram .
COPY ./nginx/default.conf /etc/nginx/conf.d/default.conf
RUN chown nobody:nogroup /app
EXPOSE 8080