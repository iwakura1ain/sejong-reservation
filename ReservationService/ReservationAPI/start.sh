#!/bin/sh

crontab /etc/cron.d/cronfile

cron &

/usr/local/bin/python3 /ReservationAPI/app.py

