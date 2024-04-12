FROM python:3.10-slim

WORKDIR /app

RUN apt-get update \
 && apt-get install unixodbc -y \
 && apt-get install unixodbc-dev -y \
 && apt-get install freetds-dev -y \
 && apt-get install freetds-bin -y \
 && apt-get install tdsodbc -y \
 && apt-get install --reinstall build-essential -y

RUN echo "[FreeTDS]\n\
Driver = /usr/local/lib/libtdsodbc.so\n\
Setup = /usr/local/lib/libtdsS.so" >> /etc/odbcinst.ini

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY . /app/

CMD ["python", "app.py"]
