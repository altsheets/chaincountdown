# As docker can only execute one CMD 
# and when I try to trick it with 'sh -c ...' the CTRL-C stopped working
# this file gets executed at each start of the docker container

# remove if exists
FOLDER="chaincountdown"
[ -d "$FOLDER" ] && rm -r $FOLDER

# clone newest version from github  
/usr/bin/git clone https://github.com/altsheets/chaincountdown

# start server
/usr/bin/python chaincountdown/server.py