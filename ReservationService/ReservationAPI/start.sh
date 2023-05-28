#!/bin/sh

# add crontab
crontab /etc/cron.d/cronfile

# start cron
cron &

# start reservationservice
/usr/local/bin/python3 /ReservationAPI/app.py

