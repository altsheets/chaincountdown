echo
echo Setting ssh password - see tutum/debian for details
/set_root_pw.sh

echo
echo Starting the sshd daemon to allow ssh login into this container
/usr/sbin/sshd -D &

echo
echo run altsheets/chaincountdown server from newest sources
/clonethenrunserver.sh
