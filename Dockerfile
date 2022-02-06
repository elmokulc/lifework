FROM continuumio/miniconda3:latest

SHELL ["/bin/bash", "--login", "-c"]

ADD environment.yml /tmp/environment.yml
RUN conda env update -f /tmp/environment.yml --prune
