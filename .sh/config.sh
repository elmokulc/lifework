#!/bin/bash
#  Conda parameters 
export CONDA_ENV=jupyter_book

# Git forge parameters
export GIT_FORGE_USERNAME=elmokulc
export GIT_FORGE_REPO_NAME=lifework

#  Registry parameters
export DOCKER_REGISTRY_URL=ghcr.io
export DOCKER_REGISTRY_USERNAME=elmokulc
export DOCKER_REGISTRY_GROUP=""
export IMAGE_NAME=lifework
export TAG=latest
export BROWSER=firefox

# Repo parameters
export REPO_REGISTRY=$(DOCKER_REGISTRY_URL)/$(DOCKER_REGISTRY_USERNAME)
# export REPO_REGISTRY=$(DOCKER_REGISTRY_URL)/$(DOCKER_REGISTRY_GROUP)/$(GIT_FORGE_REPO_NAME)

# # Repo parameters
# # export REPO_REGISTRY=$DOCKER_REGISTRY_URL/$DOCKER_REGISTRY_GROUP/$GIT_FORGE_REPO_NAME
# if [ -z "$DOCKER_REGISTRY_GROUP" ];  
#     then \
#         export REPO_REGISTRY=$DOCKER_REGISTRY_URL/$DOCKER_REGISTRY_USERNAME && \
#         echo $REPO_REGISTRY; \
#     else \
#         export REPO_REGISTRY=$DOCKER_REGISTRY_URL/$DOCKER_REGISTRY_GROUP/$GIT_FORGE_REPO_NAME && \
#         echo $REPO_REGISTRY; \
#     fi
# var=$DOCKER_REGISTRY_GROUP; \
# [ -z "$var" ] && REPO_REGISTRY=$(echo $DOCKER_REGISTRY_URL/$DOCKER_REGISTRY_USERNAME) && echo $REPO_REGISTRY 

