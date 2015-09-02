# docker related

## start manually
    docker run -p 8888:8888 -t -i altsheets/chaincountdown
    
## start manually with ssh login
    docker run -p 8888:8888 -p 2222:22 -t -i altsheets/chaincountdown sh withssh.sh
See [tutum/debian](https://github.com/tutumcloud/tutum-debian) for details.

## start with systemd
create service

	wget https://raw.githubusercontent.com/altsheets/chaincountdown/master/docker/chaincountdown.service
    cp chaincountdown.service /etc/systemd/system
    
    sudo systemctl enable /etc/systemd/system/chaincountdown.service
    sudo systemctl start chaincountdown.service
    
see logging

    journalctl -f -u chaincountdown.service
    
remove it

    sudo systemctl stop chaincountdown.service
    sudo systemctl disable /etc/systemd/system/chaincountdown.service
    rm /etc/systemd/system/chaincountdown.service

   

## Dockerfile
The [Dockerfile](../Dockerfile) contains all instructions for building the 452MB image 'altsheets/chaincountdown'

## dockerbuild.sh for altsheets/chaincountdown
[dockerbuild.sh](dockerbuild.sh) creates folder dockerCCD (if not exist), cd's into it, wget's the Dockerfile, builds the image, and starts the container.

    rm -f dockerbuild.sh* dockerCCD/dockercheatsheet.txt*
    wget https://raw.githubusercontent.com/altsheets/chaincountdown/master/docker/dockerbuild.sh
    chmod u+x dockerbuild.sh
    ./dockerbuild.sh
    
## dockercheatsheet.txt
After CTRL-C of the server in dockerbuild.sh, [dockercheatsheet.txt](dockercheatsheet.txt) is automatically wget'ted and cat'ted.  
It shows important docker commands.

## clonethenrunserver.sh
[clonethenrunserver.sh](clonethenrunserver.sh) is wget'ted and run INSIDE the docker container.  
It removes the old sourcecode (if exists), clones the newest source code from github, and starts the python server.

## feedback
I am new to docker. Please give feedback!
 