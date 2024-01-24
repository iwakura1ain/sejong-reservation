FROM python:3.10.6

WORKDIR /ReservationAPI

RUN wget https://r.mariadb.com/downloads/mariadb_repo_setup

# RUN echo "ad125f01bada12a1ba2f9986a21c59d2cccbe8d584e7f55079ecbeb7f43a4da4  mariadb_repo_setup" | sha256sum -c -

RUN chmod +x mariadb_repo_setup

RUN ./mariadb_repo_setup # --mariadb-server-version="mariadb-11.2.1"

RUN apt install -y libmariadb3 libmariadb-dev cron

COPY ./ReservationService/ReservationAPI/requirements.txt /ReservationAPI/requirements.txt

#RUN pip install --upgrade pip

RUN pip install --upgrade --no-cache-dir -r requirements.txt

# copy files before running cronjob
COPY ./ReservationService/ReservationAPI /ReservationAPI/

COPY ./Common/service.py /ReservationAPI/service.py

# cronjob after all files are copied
COPY ./ReservationService/ReservationAPI/cronfile /etc/cron.d/cronfile

RUN chmod 0644 /etc/cron.d/cronfile

#RUN touch /var/log/cron.log

#RUN crontab /etc/cron.d/cronfile

#RUN cron &

#CMD ["python3","app.py"]
RUN chmod 777 start.sh

HEALTHCHECK --interval=5m --timeout=3s CMD curl -f http://localhost/ || exit 1

EXPOSE 5000

CMD ./start.sh

