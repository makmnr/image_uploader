# Image Uploader
Description

### Requirements

### Setup

### Usage

### Developers
All apis are in the api directory, business logic is in tasks  folder, utils folder contain common functions, services contain all AWS resource service interactions, models represents each object, constants contains contanst (for now mainly env variables as well combined) 

#### Install awslocal
pip install awscli-local 
#### Start localstack in docker
docker run -d -p 4566:4566 -p 4510-4559:4510-4559 -p 8080:8080 -v /var/run/docker.sock:/var/run/docker.sock localstack/localstack
#### For localstack terraform deployment
pip install terraform-local
#### run command "make deploy_local" from root directory in terminal
