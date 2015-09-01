FROM tutum/debian:jessie

LABEL Name="ChainCountDown.py"
LABEL Description="A Blockchain aware countdown timer - rendered as a configurable image. Comes with its own webserver."
LABEL Sourcecode="https://github.com/altsheets/chaincountdown"
LABEL Example="http://altsheets.ddns.net:8888"
LABEL Password="tutum/debian:jessie says ... First time you run your container, a random password is generated for user root: docker run tutum/debian"

MAINTAINER @altsheets

RUN apt-get -y update && apt-get -y install \
  sudo \
  python \
  python-pip \
  python-imaging \
  git \
  wget

RUN sudo pip install Pillow

RUN wget https://raw.githubusercontent.com/altsheets/chaincountdown/master/docker/clonethenrunserver.sh

EXPOSE 8888

CMD ["/bin/sh", "clonethenrunserver.sh"]

