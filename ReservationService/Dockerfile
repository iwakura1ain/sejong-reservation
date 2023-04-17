FROM python:3.10.6
# https://hub.docker.com/_/python

WORKDIR /usr/src/app

COPY requirements.txt ./

# upgrade pip to prevent warning
RUN pip install --upgrade pip
# install requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn","app:app","--host","0.0.0.0","--port","5555","--reload"]
