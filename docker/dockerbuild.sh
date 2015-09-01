mkdir dockerCCD
cd dockerCCD
wget https://raw.githubusercontent.com/altsheets/chaincountdown/master/Dockerfile
docker build -t altsheets/chaincountdown .
docker run -p 8888:8888 -t -i altsheets/chaincountdown

