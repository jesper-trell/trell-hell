FROM python:3.8.5
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN apt-get update
RUN apt-get -y install npm
RUN pip3 install -r requirements.txt
COPY . /code/