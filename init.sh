#!/bin/bash
docker rm -f $(docker ps -aq)
docker build . -t chat:1.0 -f chat/Dockerfile
docker-compose up
