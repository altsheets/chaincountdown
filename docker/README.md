# docker related

## start manually
    docker run -p 8888:8888 -t -i altsheets/chaincountdown
    
## start manually with ssh login
    docker run -p 8888:8888 -p 2222:22 -t -i altsheets/chaincountdown sh withssh.sh
See [tutum/debian](https://github.com/tutumcloud/tutum-debian) for details.

## start with systemd
not ready yet

    cp chaincountdown_systemd.service /etc/systemd/system

## Dockerfile
The [Dockerfile](../Dockerfile) contains all instructions for building the 452MB image 'altsheets/chaincountdown'

## dockerbuild.sh for altsheets/chaincountdown
[dockerbuild.sh](dockerbuild.sh) creates folder dockerCCD (if not exist), cd's into it, wget's the Dockerfile, builds the image, and starts the container.

    rm -f dockerbuild.sh* dockerCCD/dockercheatsheet.txt*
    wget wget https://raw.githubusercontent.com/altsheets/chaincountdown/master/docker/dockerbuild.sh
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
 