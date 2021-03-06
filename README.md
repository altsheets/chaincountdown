# chaincountdown.py v14.1

Time estimation to targetblock of nxt/hz. 

Image rendered at request. Comes with httpserver.
Choose heading, fontsizes, fontface, colors.

Built for for the nxthacks voting, and beyond. Useful e.g. for voting, and phased transactions.

**New:** 
* Complete docker solution
* incl. systemd autostart! 
* Adjusted to new faster NXT blockspeed.

## shortversion

Put live-rendered [image](http://altsheets.ddns.net:8888/nxt/10000000.png?heading=funfact:%2010%20mio%20nxtblocks) into any [website](https://nxtforum.org/index.php?topic=9735).

![example image](http://altsheets.ddns.net:8888/nxt/10000000.png?heading=funfact:%2010%20mio%20nxtblocks)  
Is github making them static? Then here is the direct link:  
http://altsheets.ddns.net:8888/nxt/10000000.png?heading=funfact:%2010%20mio%20nxtblocks 


### old example (all this was made for nxthacks2015 voting countdown)

This image is generated automatically, and always up-to-date:  
http://altsheets.ddns.net:8888/nxt/495997.png?heading=nxthacks%20voting   

The image can be placed into any webpage, like here:  
http://altsheets.ddns.net/assetgraphs/

## quickstart

    python server.py

For dependencies, see the apt-get install part of the [Dockerfile](docker/Dockerfile).

## autostart

See the [daemon/README-serverinstall.txt](daemon/README-serverinstall.txt) or use a docker image: ...
    
## docker

See [DockerHub](https://hub.docker.com/r/altsheets/chaincountdown/) and [Dockerfile](docker/Dockerfile) and [docker/README.md](docker/README.md).  

Start the server manually:

    docker run -p 8888:8888 -t -i altsheets/chaincountdown
    
Autostart as **systemd** service - for details see [docker#start-with-systemd](docker#start-with-systemd)

	wget https://raw.githubusercontent.com/altsheets/chaincountdown/master/docker/chaincountdown.service
    sudo cp chaincountdown.service /etc/systemd/system
    sudo systemctl enable /etc/systemd/system/chaincountdown.service
    reboot

## license

Placed under my [giveback license v05](http://altsheets.ddns.net/give). Please give generously. Thx.

## manual

Much more infos, e.g. on how to choose better colors, sizes, font, etc:  
http://altsheets.ddns.net:8888

**TL;DR:**
 
** A Blockchain aware countdown timer !**

shorturl for this: [2020.fm/ccd](http://2020.fm/ccd)

