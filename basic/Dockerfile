FROM ubuntu:latest

RUN apt-get update && apt-get install -y python3 python3-pip python3-dev
COPY . /opt
WORKDIR /opt
RUN pip3 install oss2 boto3

