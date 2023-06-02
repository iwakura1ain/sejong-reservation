#!/bin/bash

echo "========= DEPLOYING =========" | tee Actions-Test/testing.txt 

git pull | tee Actions-Test/testing.txt 

docker-compose build --no-cache | tee Actions-Test/testing.txt 

docker-compose up --force-recreate --detach | tee Actions-Test/testing.txt 

echo "========= DEPLOYMENT DONE =========" | tee Actions-Test/testing.txt 


