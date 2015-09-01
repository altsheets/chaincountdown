# As docker can only execute one CMD 
# this whole script gets executed at each start of the docker container

echo 
echo CMD clonethenrunserver.sh
echo 

FOLDER="chaincountdown"
if [ -d $FOLDER ];
then
   cd $FOLDER
   echo Updating to newest source code from GitHub:
   /usr/bin/git pull
else
   echo Cloning newest source code from GitHub:
   /usr/bin/git clone https://github.com/altsheets/chaincountdown
fi

echo
echo Starting Server:
echo If you have started the container with -t -i ... press CTRL-C to stop. 
echo If not ... then you have to kill it with 'killall -9 docker'.
echo
 
/usr/bin/python chaincountdown/server.py