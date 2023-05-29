#!/bin/sh

# add crontab
crontab /etc/cron.d/cronfile

# start cron
cron &

# start reservationservice
# /usr/local/bin/python3 /ReservationAPI/app.py
gunicorn --bind 0.0.0.0:5000 wsgi:APP
