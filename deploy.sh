rm -rf ./owo/static/*.gz
gzip -r -k -f ./owo/static/
docker-compose up --build