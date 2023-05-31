FROM python:3.11.2-buster

ENV PYTHONBUFFERED 1

WORKDIR /AlertAPI

COPY ./AlertService/AlertAPI/requirements.txt /AlertAPI/requirements.txt

RUN python3 -m pip install --upgrade pip

RUN pip install --no-cache-dir --upgrade -r /AlertAPI/requirements.txt

COPY ./AlertService/AlertAPI /AlertAPI/

#HEALTHCHECK --interval=5m --timeout=3s CMD curl -f http://localhost/ || exit 1

# CMD ["python3", "app.py"]
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:APP"]
