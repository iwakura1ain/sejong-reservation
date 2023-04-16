# ReservationService
(다른 서비스랑 돌아가는지 확인x)

## Run container
```
# cd into directory
cd ReservationService/
# build image
sudo docker build . -t reservation
# run container
sudo docker run --name ReservationService -p 8000:8000 reservation 
# try curling localhost
curl localhost:8000 ## "hello from Reservation"
```

## Stop container
```
# check name of the container
sudo docker ps 
# stop and remove container
sudo docker stop ReservationService
sudo docker rm ReservationService
# ... or just force remove directly
sudo docker rm ReservationService -f
```