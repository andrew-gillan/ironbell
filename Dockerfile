############################################################
# Dockerfile to run a Django-based web application
# Based on an Ubuntu Image
############################################################

# Set the base image to use to Ubuntu
FROM ubuntu:14.04

# Set the file maintainer (your name - the file's author)
MAINTAINER Andrew Gillan <andrew.gillan@com1.io>

# Install packages
RUN apt-get update && apt-get install -y \
    python \
    python-pip \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

RUN pip install django==1.6.11
RUN pip install suit==2.0.2
RUN pip install django_extensions==1.6.1
RUN pip install djangorestframework==2.4.8

# Clone project from github
# RUN git clone https://github.com/andrew-gillan/ironbell.git /usr/local/ironbell

EXPOSE 8000

# Setup User to match Host User, and give superuser permissions (not portable unless build by each use themself)
ARG USER_ID=0
RUN useradd developer -u ${USER_ID} -g sudo
RUN echo 'developer ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
USER ${USER_ID}

VOLUME /usr/local/ironbell

