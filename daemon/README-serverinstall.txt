# v10.02
#
# goal: run as normal user 'ccdserve'
#

# creating group and user:
sudo -i 
groupadd ccdserve
usermod -G ccdserve root
useradd ccdserve -g ccdserve
passwd ccdserve

# into /opt/ so that it can be run at startup  
mkdir /opt/altsheets/

# get it from my github
cd /opt/altsheets/
git clone https://github.com/altsheets/chaincountdown.git

# if it was transferred by FTP, this might help:
sudo apt-get update; sudo apt-get install dos2unix
dos2unix /opt/altsheets/chaincountdown/*.py

# allow the user to write to /opt/altsheets/  for logging.
chown -R ccdserve:ccdserve /opt/altsheets/
chmod g+w /opt/altsheets/ 

# this is probably already set in the github repository
chmod ug+x /opt/altsheets/chaincountdown/server.py
chmod ug+x /opt/altsheets/chaincountdown/imaging.py

#
# manual start (stop with Ctrl-C):
/opt/altsheets/chaincountdown/server.py

# or on separate screen (leave with Ctrl-A D)
sudo apt-get update; sudo apt-get install screen
screen -S CCD /opt/altsheets/chaincountdown/server.py

# generate the allfonts.png image for your /fonts/ folder:
/opt/altsheets/chaincountdown/imaging.py

# all good (apart from that it is running as root)? 
# Then you can move on:


#
# autostart, run as ccdserve
#

# logging to /opt/altsheets/chaincountdown.log
# using 'daemon' to run this as a different user
apt-get install daemon

# testing
daemon -n CCD -u ccdserve -o /opt/altsheets/chaincountdown.log /opt/altsheets/chaincountdown/server.py

# check if you can see it logging:
tail /opt/altsheets/chaincountdown.log -f

# if yes, then you add this line to '/etc/rc.local'
sudo nano /etc/rc.local
# anywhere above the 'exit 0':
daemon -n CCD -u ccdserve -o /opt/altsheets/chaincountdown.log /opt/altsheets/chaincountdown/server.py

# reboot.
# Login as anyone. 
# Check if it is logging when you call it at http://yourhost:8888
# and as which user it is running (first column)
ps aux | grep chaincountdown

# P.S.: killing it
ps aux | grep chaincountdown
sudo daemon -n CCD -u ccdserve --stop

# update sourcecode to the newest version:
cd /opt/altsheets/chaincountdown/
git pull


# unsolved problem: 
# Only stderr gets logged, all other print output disappears. Don't know why.

# Please give feedback!

