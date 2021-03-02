FROM ubuntu:16.04
RUN apt-get update -y
RUN apt-get install python -y
RUN apt-get install python-pip -y
COPY requirements.txt /home/requirements.txt
RUN pip install -r /home/requirements.txt
COPY . /home
ENTRYPOINT FLASK_APP=/home flask run --host=0.0.0.0