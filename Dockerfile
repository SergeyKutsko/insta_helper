FROM sergeykutsko86/base_image:latest
USER nobody
RUN sudo mkdir -p /app
WORKDIR /app
COPY requirements.txt .
RUN sudo apt-get update
RUN sudo apt-get install gettext -y
RUN sudo pip install -r requirements.txt

EXPOSE 8080