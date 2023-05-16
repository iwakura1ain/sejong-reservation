FROM python:3.11.2-buster

ENV PYTHONBUFFERED 1

COPY ./AdminService/AdminAPI /AdminAPI/

COPY ./Common/service.py /AdminAPI/service.py

WORKDIR /AdminAPI

RUN ls .

RUN apt update

RUN apt install wget

RUN wget https://r.mariadb.com/downloads/mariadb_repo_setup

RUN echo "ad125f01bada12a1ba2f9986a21c59d2cccbe8d584e7f55079ecbeb7f43a4da4  mariadb_repo_setup" | sha256sum -c -

RUN chmod +x mariadb_repo_setup

RUN ./mariadb_repo_setup --mariadb-server-version="mariadb-10.6"

RUN apt install libmariadb3 libmariadb-dev --yes

RUN python3 -m pip install --upgrade pip

RUN python3 -m pip install -r requirements.txt

EXPOSE 5000

CMD ["python3", "app.py"]

