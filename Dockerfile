FROM continuumio/miniconda3:latest

RUN apt-get update && apt-get install libgl1 -y && \
    apt install build-essential -y && \
    apt-get install ffmpeg libsm6 libxext6  -y && \
    apt install libspatialindex-dev -y && \
    apt-get install openscad blender -y && \
    apt-get install pkg-config -y && \
    apt-get install libcairo2-dev -y 
SHELL ["/bin/bash", "--login", "-c"]

ADD environment.yml /tmp/environment.yml
RUN conda env update -f /tmp/environment.yml --prune
RUN echo "Your python path echo $(which python)"
RUN conda activate base
RUN echo "Your python path echo $(which python)"
RUN echo "$(conda env list)"
RUN python -m pip install git+https://github.com/elmokulc/GBU_pose_classifier.git
