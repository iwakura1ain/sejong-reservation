FROM python:3.10.6
# https://hub.docker.com/_/python

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN wget https://r.mariadb.com/downloads/mariadb_repo_setup

RUN echo "ad125f01bada12a1ba2f9986a21c59d2cccbe8d584e7f55079ecbeb7f43a4da4  mariadb_repo_setup" | sha256sum -c -

RUN chmod +x mariadb_repo_setup

RUN ./mariadb_repo_setup --mariadb-server-version="mariadb-10.6"

RUN apt install libmariadb3 libmariadb-dev --yes



# upgrade pip to prevent warning
RUN pip install --upgrade pip
# install requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn","app:app","--host","0.0.0.0","--port","5555","--reload"]
