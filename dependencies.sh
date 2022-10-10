#!/bin/bash

# pipenv lock --requirements > requirements.txt

#* BUILD IMAGE

docker build --progress=plain -t fast_api_base .

#*RUN IMAGE
docker run  -d  -p 8000:8000 fast_api_base