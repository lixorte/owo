find . -type f -name '*.gz' -delete
gzip -r -k -f ./owo/static/
docker-compose up --build