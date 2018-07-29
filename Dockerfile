FROM python:3.5

RUN apt-get update
RUN apt-get install mysql-server

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3", "/runserver.py"]

EXPOSE 8888
