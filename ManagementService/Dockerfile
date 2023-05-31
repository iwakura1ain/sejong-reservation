FROM python:3.11.2-buster

ENV PYTHONBUFFERED 1

WORKDIR /ManagementAPI

RUN wget https://r.mariadb.com/downloads/mariadb_repo_setup

RUN echo "ad125f01bada12a1ba2f9986a21c59d2cccbe8d584e7f55079ecbeb7f43a4da4  mariadb_repo_setup" | sha256sum -c -

RUN chmod +x mariadb_repo_setup

RUN ./mariadb_repo_setup --mariadb-server-version="mariadb-10.6"

RUN apt install libmariadb3 libmariadb-dev -y

COPY ./ManagementService/ManagementAPI/requirements.txt /ManagementAPI/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /ManagementAPI/requirements.txt

COPY ./ManagementService/ManagementAPI /ManagementAPI/

COPY ./Common/service.py /ManagementAPI/service.py

#HEALTHCHECK --interval=5m --timeout=3s CMD curl -f http://localhost/ || exit 1

# CMD ["python3", "app.py"]
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:APP"]

