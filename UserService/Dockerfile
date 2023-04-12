FROM python:3.11.2-buster

ENV PYTHONBUFFERED 1

COPY UserAPI /UserAPI/

WORKDIR /UserAPI

RUN ls .

RUN apt update


RUN apt install libmariadb3 libmariadb-dev 

RUN python3 -m pip install --upgrade pip

RUN python3 -m pip install -r requirements.txt

EXPOSE 5000

RUN

CMD ["python", " app.py"]



