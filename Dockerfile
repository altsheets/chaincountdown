FROM tutum/debian:jessie

LABEL Name="ChainCountDown.py"
LABEL Description="A Blockchain aware countdown timer - rendered as a configurable image. Comes with its own webserver."
LABEL Sourcecode="https://github.com/altsheets/chaincountdown"
LABEL Example="http://altsheets.ddns.net:8888"
LABEL Password="First time you run your container, a random password is generated for user root. To get the password: docker logs CONTAINER_ID"

MAINTAINER @altsheets

RUN apt-get -y update
RUN apt-get -y install sudo python python-pip python-imaging git wget
RUN sudo pip install Pillow

RUN rm -f /usr/local/bin/run.sh
RUN wget https://raw.githubusercontent.com/altsheets/chaincountdown/master/docker/run.sh --output-document=/usr/local/bin/run.sh
RUN chmod u+x /usr/local/bin/run.sh

EXPOSE 8888

# at each start, delete folder, get new git clone, start server:
CMD ["run.sh"]

