#!/bin/bash

#
# Upgrades to a newer version from github
# 
# N.B.: Not sure you already want to run this as a script in one go.
#       Please advise me ...
#

cd /opt/altsheets/
daemon -n CCD -u ccdserve --stop

# cp -r chaincountdown chaincountdown_v10
cp -r chaincountdown chaincountdown_OLD

# mv chaincountdown.log chaincountdown_v10.log
mv chaincountdown.log chaincountdown_OLD.log

cd chaincountdown
git pull
cd ..

daemon -n CCD -u ccdserve -o /opt/altsheets/chaincountdown.log /opt/altsheets/chaincountdown/server.py
ps aux | grep chaincountdown
# has (daemon) & has (python)?

echo
echo http://altsheets.ddns.net:8888
echo Ctrl-click all @examples, and all errors.html
echo Check the @history - try out the recent changes.
echo
echo "tail -f /opt/altsheets/chaincountdown.log"
 
tail -f /opt/altsheets/chaincountdown.log
# has (Running this as: 'ccdserve') and has(Started httpserver on port:  8888) ?
