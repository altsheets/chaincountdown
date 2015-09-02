# Docker quickstart
You really only need the very first command here. All the other stuff is for advanced purposes.

## start manually
    docker run -p 8888:8888 -t -i altsheets/chaincountdown
    
## start manually with ssh login
    docker run -p 8888:8888 -p 2222:22 -t -i altsheets/chaincountdown sh withssh.sh
See [tutum/debian](https://github.com/tutumcloud/tutum-debian) for details.

## start with systemd
Do all this as root:  

Create service

	wget https://raw.githubusercontent.com/altsheets/chaincountdown/master/docker/chaincountdown.service
    cp chaincountdown.service /etc/systemd/system
    systemctl enable /etc/systemd/system/chaincountdown.service
    
Test it manually

    systemctl start chaincountdown.service
    journalctl -f -n 25 -u chaincountdown.service
    systemctl stop chaincountdown.service
    journalctl -f -n 25 -u chaincountdown.service

Test autorun

	reboot
	journalctl -f -n 25 -u chaincountdown.service
	 
Remove it

    systemctl disable /etc/systemd/system/chaincountdown.service
    rm /etc/systemd/system/chaincountdown.service


# Docker for experts

## Dockerfile
The [Dockerfile](Dockerfile) contains all instructions for building the 454MB image '[altsheets/chaincountdown](https://hub.docker.com/r/altsheets/chaincountdown/)' (hosted at DockerHub). It was built with:

## dockerbuild.sh for altsheets/chaincountdown
[dockerbuild.sh](dockerbuild.sh) creates folder dockerCCD (if not exist), cd's into it, wget's the Dockerfile, builds the image, and starts the container.

    rm -f dockerbuild.sh* dockerCCD/dockercheatsheet.txt*
    wget https://raw.githubusercontent.com/altsheets/chaincountdown/master/docker/dockerbuild.sh
    sh ./dockerbuild.sh
    
## dockercheatsheet.txt
After CTRL-C of the server in dockerbuild.sh, [dockercheatsheet.txt](dockercheatsheet.txt) is automatically wget'ted and cat'ted.  
It shows important docker commands.

## clonethenrunserver.sh
[clonethenrunserver.sh](clonethenrunserver.sh) is wget'ted and run INSIDE the docker container.  
It removes the old sourcecode (if exists), clones the newest source code from github, and starts the python server.

## feedback
I am new to docker. Please give feedback!
 