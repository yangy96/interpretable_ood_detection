# Artifact Evaluation 
Artifact evaluation for *Interpretable Detection of Distribution Shifts in Learning Enabled Cyber-Physical Systems*. 

Please follow the steps below to reproduce the results.

## Step 1) Download the repo

`git clone https://github.com/yangy96/interpretable_ood_detection.git`

## Step 1) Environment set up

This step is for seting up the environment and installing the dependancies for running our experiments. 

Please choose one of these: virtual environment (Preferred) or docker

### Virtual Environment (Preferred)
1. Create a virtual environment: `python3 -m venv env`
2. Activate environment: `source env/bin/activate`
3. Update pip tool: `pip3 install -U pip`
4. To install all packages: `pip install -r requirements.txt`

After finishing the experiments, to leave the virtual environment, if using venv, `deactivate`

### Docker
1. install [Docker](https://docs.docker.com/get-docker/) on your machine 
2. To build a docker image: `docker build -t reproduce-test .` <br>
3. To run the docker container and open an interactive session with docker: `docker run -i -t --gpus all --name temp_test --rm reproduce-test /bin/bash`

After finishing the experiments, to leave the docker environment, 
run `exit` <br>

## Step 2) To reproduce our OOD experiments 

### To run OOD experiments to detect change in carla simulation (section 6.1 & 6.2)
1. `cd interpretable_ood_detection/cd carla_experiments`

2. Download CARLA data under this link: https://drive.google.com/file/d/1I1Rm-EziREPiBDAQSraYt0j_VwCbqLZE/view?usp=sharing by running 'wget -O carla_data.tar https://drive.google.com/file/d/1I1Rm-EziREPiBDAQSraYt0j_VwCbqLZE/view?usp=sharing'

(Note: the data used in this experiment is about 16GB)

3. `tar -xvf carla_data.tar`

4. Follow instructions in carla_experiments/*README.md*

### To run OOD experiments to detect perturbations by adversarial attack (section 6.3)
1. `cd interpretable_ood_detection/cd carla_adversarial_experiments`

2. Download  CARLA ADVERSARIAL data under this link: https://drive.google.com/file/d/17dKNOAQWOL3KGbv7oj0-rV8FIHcakPPU/view?usp=sharing by running - 'wget -O  carla_adversarial.tar https://drive.google.com/file/d/1I1Rm-EziREPiBDAQSraYt0j_VwCbqLZE/view?usp=sharing'
 
(Note: the data used in this experiment is about 16GB)

3. `tar -xvf carla_adversarial.tar`

4. Follow instructions in carla_adversarial_experiments/*README.md*

### To run OOD experiments for lidar data (section 7.3)
run `cd lidar_experiments` <br>
Follow instructions in lidar_experiments/*README.md*

