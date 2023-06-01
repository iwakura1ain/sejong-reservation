#!/bin/bash

git pull

docker compose build --no-cache

docker compose up --force-recreate --detach

echo "DEPLOYMENT DONE"


