
FROM tutum/debian:jessie

LABEL Name="ChainCountDown.py"
LABEL Description="A Blockchain aware countdown timer - rendered as a configurable image. Comes with its own webserver."
LABEL Sourcecode="https://github.com/altsheets/chaincountdown"
LABEL Example="http://altsheets.ddns.net:8888"
LABEL Password="First time you run your container, a random password is generated for user root. To get the password: docker logs CONTAINER_ID"

MAINTAINER @altsheets

RUN apt-get -y update && apt-get -y install sudo python python-pip python-imaging git && sudo pip install Pillow

RUN git clone https://github.com/altsheets/chaincountdown

EXPOSE 8888
CMD ["python", "chaincountdown/server.py"]
