FROM ubuntu:latest
MAINTAINER Austin Graham "austin.graham@ou.edu"

RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev build-essential
RUN pip3 install --upgrade pip

COPY . /src

WORKDIR /src

RUN pip3 install .
RUN python3 -c 'import nltk; nltk.download("stopwords")'
EXPOSE 80
CMD gs_up -p 80
