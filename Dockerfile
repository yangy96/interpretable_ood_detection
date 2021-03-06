FROM nvidia/cuda:11.0-base-ubuntu18.04-rc

RUN apt-get update
RUN apt-get install build-essential -y
RUN apt-get install -y python3
RUN apt-get install -y python3-pip wget unzip build-essential automake curl vim python3-dev default-jdk  git

RUN apt-get update
RUN pip3 install --upgrade pip
RUN pip3 install -U setuptools --no-cache-dir

COPY ./ /home/interpretable_ood_detection

WORKDIR /home/interpretable_ood_detection

RUN python3 --version

RUN pip install -r requirements.txt

