FROM python:3.11.2-buster

ENV PYTHONBUFFERED 1

WORKDIR /UserAPI

RUN wget https://r.mariadb.com/downloads/mariadb_repo_setup

RUN echo "ad125f01bada12a1ba2f9986a21c59d2cccbe8d584e7f55079ecbeb7f43a4da4  mariadb_repo_setup" | sha256sum -c -

RUN chmod +x mariadb_repo_setup

RUN ./mariadb_repo_setup --mariadb-server-version="mariadb-10.6"

RUN apt install libmariadb3 libmariadb-dev --yes

COPY ./UserService/UserAPI/requirements.txt /UserAPI/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /UserAPI/requirements.txt

COPY ./UserService/UserAPI /UserAPI/

COPY ./Common/service.py/ /UserAPI/service.py

CMD ["python3", "app.py"]
