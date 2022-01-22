# Artifact Evaluation 
Artifact evaluation for *Interpretable Detection of Distribution Shifts in Learning Enabled Cyber-Physical Systems*. 

Please follow the steps below to reproduce the results.

## Step 1) Download the repo and required datasets

1. `git clone https://github.com/yangy96/interpretable_ood_detection.git`

2. `cd interpretable_ood_detection/carla_experiments`

TO DO : put a download link here 

3. `cd ../`

4. `cd carla_adversarial_experiments`

TO DO: put a download link here 

5. `cd ../`

## Step 2) Environment set up

This step is for seting up the environment and installing the dependancies for running our experiments. 

Please choose one of these: Docker or virtual environment 

### Docker
1. install [Docker](https://docs.docker.com/get-docker/) on your machine 
2. To build a docker image: `docker build -t reproduce-test .` <br>
3. To run the docker container and open an interactive session with docker: `docker run -i -t --gpus all --name temp_test --rm reproduce-test /bin/bash`

After finishing the experiments, to leave the virtual environment, 
run `exit` <br>

### Virtual Environment 
1. Create a virtual environment: `python3 -m venv env`
2. Activate environment: `source env/bin/activate`
3. To install all packages: `pip install -r requirements.txt`

After finishing the experiments, to leave the virtual environment, if using venv, `deactivate`

## Step 3) To reproduce our OOD experiments 

### To run OOD experiments to detect change in carla simulation (section 6.1 & 6.2)
run `cd carla_experiments` <br>
more details could be found in *README.md* in the carla_experiments 

### To run OOD experiments to detect perturbations by adversarial attack (section 6.3)
run `cd carla_adversarial_experiments` <br>
more details could be found in *README.md* in the carla_adversarial_experiments

### To run OOD experiments for lidar data (section 7.3)
run `cd lidar_experiments` <br>
more details could be found in *README.md* in the lidar_experiments

