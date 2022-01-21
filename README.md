# Artifact Evaluation 
artifact evaluation for *Interpretable Detection of Distribution Shifts in Learning Enabled Cyber-Physical Systems*

## Firstly, please download all necessary data files to the place

`cd carla_experiments`

TO DO : put a download link here 

`cd ../`

`cd carla_adversarial_experiments`

TO DO: put a download link here 

`cd ../`

### Environment set up

#### Docker
To build a docker image: `docker build -t reproduce-test .` <br>
To run the docker container and open an interactive session with docker: `docker run -i -t --gpus all --name temp_test --rm reproduce-test /bin/bash`

If succeed, reproduce the following experiments in docker container 

#### Virtual Environment 
If there is any error occur with docker instantiation, could also run <br>
- `python3 -m venv env`
- `source env/bin/activate`
- `pip install -r requirements.txt`
and reproduce following experiments <br>

After finishing the experiments, to leave the virtual environment <br>
if using Docker container, `exit` <br>
if using venv, `deactivate`

## To run OOD experiments to detect change in carla simulation (section 6.1 & 6.2)
run `cd carla_experiments` <br>
more details could be found in *README.md* in the carla_experiments 

## To run OOD experiments to detect perturbations by adversarial attack (section 6.3)
run `cd carla_adversarial_experiments` <br>
more details could be found in *README.md* in the carla_adversarial_experiments

## To run OOD experiments for lidar data (section 7.3)
run `cd lidar_experiments` <br>
more details could be found in *README.md* in the lidar_experiments

