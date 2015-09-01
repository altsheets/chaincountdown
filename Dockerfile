
FROM tutum/debian:jessie

LABEL Name="ChainCountDown.py"
LABEL Description="A Blockchain aware countdown timer - rendered as a configurable image. Comes with its own webserver."
LABEL Sourcecode="https://github.com/altsheets/chaincountdown"
LABEL Example="http://altsheets.ddns.net:8888"
LABEL Password="First time you run your container, a random password is generated for user root. To get the password: docker logs CONTAINER_ID"

MAINTAINER @altsheets

RUN apt-get -y update && apt-get -y install sudo python python-pip python-imaging git && sudo pip install Pillow

EXPOSE 8888

# at each start, delete folder, get new git clone, start server:

CMD ["/bin/sh", 
     "-c", 
     "'rm -r chaincountdown; git clone https://github.com/altsheets/chaincountdown && python chaincountdown/server.py'"]
