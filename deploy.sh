find . -type f -name '*.gz' -delete
find ./owo/static -type f ! -name '*.gz' -exec gzip -k -f "{}" \;