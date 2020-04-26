# Docker environment
This is an example docker environment is only for developing and testing Lego.
This shouldn't be used in production.

## Dockerfile
Defines a basic docker image which is based on buster (the current stable distribution of Debian - version 10) with python 3.8.2.
The docker has a `openssh-server`.
The credentials to the docker are root:password.
Also, the docker has nc, tcpdump, and a couple of pip packages preinstalled.

## Docker compose
Starts the multiple docker images with the following logic:
A central server that runs the Lego Manager.
The Zebra's and Giraffe dockers which are running rpyc_classic.
Finally, the DNS service provides the capability to resolve the docker's IP address by their hostname.
