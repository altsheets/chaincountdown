echo
echo dockerbuild.sh for altsheets/chaincountdown
echo
echo This creates folder dockerCCD if not exist, 
echo cd s into it,
echo wget s the Dockerfile, and
echo builds the image, and 
echo starts the container.
echo
echo If you do not want to continue, press CTRL-C.
echo If you want to continue, press ENTER
read

FOLDER="dockerCCD"
if [ -d $FOLDER ];
then
   echo $FOLDER already exists, using it
else
   mkdir dockerCCD
fi

cd dockerCCD

rm -f Dockerfile*
wget https://raw.githubusercontent.com/altsheets/chaincountdown/master/Dockerfile

docker build -t altsheets/chaincountdown .
docker run -p 8888:8888 -t -i altsheets/chaincountdown

rm -f dockercheatsheet.txt*
wget -q https://raw.githubusercontent.com/altsheets/chaincountdown/master/docker/dockercheatsheet.txt
cat dockercheatsheet.txt

