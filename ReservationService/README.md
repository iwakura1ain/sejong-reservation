# ReservationService
(간단한 reservation CR_D 가능, __명세 따르지 않는 부분 있음.__)

## Deploy Locally

### Deploy with `docker compose` 
```sh
# cd into __project root__ directory
cd sejong-reservation/
# build
docker compose build
# up
docker compose up
# up without log output
docker compose up -d
# down
docker compose down
# check status
curl localhost:5555 # "hello from Reservation"
```

- (optional) 리눅스 기준 sudo 없이 돌리고 싶으면 [여기로](https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user)
- db확인하고 싶으면 브라우저에서 `localhost:9999`로 들어가서 adminer 로그인.
    - 로그인 정보 `MySQL/dbservice/testusr/1234/exampledb` 
- swagger: `localhost:5555/docs`, redoc: `localhost:5555/redoc`
- `restart: on-failure`: 배포할때는 always로 바꿔서 배포.

### Run container 
```sh
# cd into directory
cd ReservationService/
# build image
sudo docker build . -t reservation
# run container
sudo docker run --name ReservationService -p 8000:8000 reservation 
# try curling localhost
curl localhost:8000 ## "hello from Reservation"
```

### Stop container
```sh
# check name of the container
sudo docker ps 
# stop and remove container
sudo docker stop ReservationService
sudo docker rm ReservationService
# ... or just force remove directly
sudo docker rm ReservationService -f
```
