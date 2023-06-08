#!/bin/bash

sudo whoami

echo "========= DEPLOYING =========" | tee -a deploy.log

sudo docker-compose build --no-cache | tee -a deploy.log

sudo docker-compose up --force-recreate --detach | tee -a deploy.log

echo "========= DEPLOYMENT DONE =========" | tee -a deploy.log


