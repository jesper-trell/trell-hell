FROM python:3.8.5
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN apt-get update
RUN apt-get install -y libsm6 libxext6 libxrender-dev
RUN pip3 install -r requirements.txt
RUN pip install opencv-python-headless
RUN pip install opencv-python
RUN apt -y install npm
COPY . /code/