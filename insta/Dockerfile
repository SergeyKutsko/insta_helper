FROM python:3.10
USER nobody
RUN mkdir -p /app
WORKDIR /app
COPY requirements.txt .
RUN apt-get update
RUN apt-get install gettext -y
RUN pip install -r requirements.txt

RUN rm /etc/nginx/sites-enabled/default
RUN rm /etc/nginx/sites-available/default
COPY . .
COPY ./nginx/default.conf /etc/nginx/conf.d/default.conf
RUN sudo chown nobody:nogroup /app
EXPOSE 8080