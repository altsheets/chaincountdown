# As docker can only execute one CMD 
# and when I try to trick it with 'sh -c ...' the CTRL-C stopped working
# this file gets executed at each start of the docker container


FOLDER="chaincountdown"
if [ -d $FOLDER ];
then
   rm -r $FOLDER
   echo Removed old source folder.
fi

echo Cloning newest source code from GitHub:
/usr/bin/git clone https://github.com/altsheets/chaincountdown

echo Starting Server:
echo If you have started the container with -t .. just press CTRL-C to stop. 
echo If not .. then you have to kill it with 'killall -9 docker'.
echo 
/usr/bin/python chaincountdown/server.py