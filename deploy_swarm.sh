#!/bin/bash
echo "========= DEPLOYING =========" | tee -a deploy.log

sudo whoami | tee -a deploy.log 

date | tee -a deploy.log 

sudo docker-compose build | tee -a deploy.log

sudo docker-compose push | tee -a deploy.log 

#sudo docker-compose up --force-recreate --detach | tee -a deploy.log

sudo docker stack deploy --compose-file docker-compose.yaml sejong-reservation | tee -a deploy.log 

echo "========= DEPLOYMENT DONE =========" | tee -a deploy.log


