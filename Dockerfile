FROM python:3.10.8

#maintainer

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONBUFFERED 1

#directory to store app source code
RUN mkdir /src

#switch to /app directory so that everything runs from here
WORKDIR /src

#copy the app code to image working directory
COPY ./src /src
# COPY /etc/ssl/certs /usr/local/share/ca-certificates/
RUN update-ca-certificates
#let pip install required packages
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y ca-certificates