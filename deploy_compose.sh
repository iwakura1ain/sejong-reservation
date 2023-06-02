#!/bin/bash

sudo whoami

echo "========= DEPLOYING =========" | tee -a Actions-Test/testing.txt 

sudo docker-compose build --no-cache | tee -a Actions-Test/testing.txt 

sudo docker-compose up --force-recreate --detach | tee -a Actions-Test/testing.txt 

echo "========= DEPLOYMENT DONE =========" | tee -a Actions-Test/testing.txt 


