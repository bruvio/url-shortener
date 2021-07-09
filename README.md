# url-shortener

creating my own url shortener that runs also from a docker container.

The app will hash a given url using the hashids open source library and then store the shortened url in a MySQL database

### 1. Initial Setup

**Quick Setup** (prereq: `git, python3.8`,`docker` )

```bash
git clone <reponame>
python -m venv .env3.8
pip install -r requirements.txt
```

#### Project Structure:

Mono-repo style

```
├──app/
    ├── __init__.py
    ├── ─wsgi.py
    ├── tests
    │   ├── test_app.py
    │   ├── conftest.py
    └── src
        ├── __init__.py
        ├── app.py
        ├── db.py
        ├── schema.sql
        └── utils
            ├── __init__.py
            ├── queries.py
├──Dockerfile
├──docker-compose.yml
├──pytest-compose.yml
├──.pylintrc
├──.gitignore
├──.pre-commit-config.yaml
├──isort.cfg
├──requirements-dev.txt
├──README.md
├──.github


```

- `app/wsgi.py`: contains the entrypoint for the application.
- `app/tests/`: Tests for basic operations on the app.
- `app/utils/`: Helpers functions
- `app/src/`: source file of the app
- `app/src/app.py`: main file
- `app/src/db.py`: script to initilize a MySQL database
- `app/src/schema.sql`: file that defines the schema of the database
- `Dockerfile`: dockerfile for building an image and future deployment to AWS (or other cloud provider)
- `pytest-Dockerfile`: dockerfile for local testing
- `.github`: folder containing 2 workflows for automation: one tests the app in a github runner, the second builds a docker image

### 4. Starting the environment

to start the app locally
from the terminal run

`./run.sh`

the service will start listening at

`http://127.0.0.1:8000`

copy in the form the url you want to shortner and you will get a new tiny url

this url is also stored in a table to create stats.
the stats table is accessible by clicking on the stats button (top-left of the page)

### 5. Building Docker image

to create a docker image run

```
docker build -t bruvio-url-shortener .
```

### 6. Running app from container locally

to run the app from the container locally run from the terminal

```
docker run -i -p 8000:8000 -d bruvio-url-shortener
```

and then from the browser visit

```
localhost:8000
```

### 7. local testing using a docker container

to run local test using a docker container run

```
docker-compose up
```

### 8. deploy to AWS

to deploy to AWS, this is how I would do it

1.

first build an image

```
IMAGE_VERSION=${1:-latest} IMAGE_NAME="bruvio-url-shortener" docker build -t $IMAGE_NAME:$IMAGE_VERSION .
```

2.

once the image is build push it to dockerhub

3.

Create a cloudformation template to generate Roles, for example something like this

```
export REGION="us-east-1"

echo ""
echo "creating role stack"
echo ""
aws cloudformation create-stack --capabilities CAPABILITY_IAM --stack-name ecs-roles --template-body file:///create_IAM_roles.yml

aws cloudformation wait stack-create-complete --stack-name ecs-roles
```

and export the roles, for example:

```echo "AutoscalingRole: $AutoscalingRole"
echo "EC2Role: $EC2Role"
echo "ECSRole: $ECSRole"
echo "ECSTaskExecutionRole: $ECSTaskExecutionRole"
```

4.

add / extend permissions for example to access SSM parameter store, Xray,....

5.

crete a VPC stack, for example

```
echo ""
echo "creating vpc stack"
echo ""
aws cloudformation create-stack --capabilities CAPABILITY_IAM --stack-name ecs-core-infrastructure --template-body file:///core-infrastructure-setup.yml

aws cloudformation wait stack-create-complete --stack-name ecs-core-infrastructure
```

and export relevant info from the stack outputs, like vpc, subnets,...

6.

create a ALB (application load balancer) stack, for example

```
echo ""
echo "creating alb stack"
echo ""
aws cloudformation create-stack \
--stack-name external-alb \
--template-body file:///alb-external.yml

aws cloudformation wait stack-create-complete --stack-name external-alb
```

and export relevant info from the stack outputs, like alb security group id, dns names,...

7.

create a cluster

8.

create a task definition using the docker image (either coming from ecr or dockerhub)

9.

create a service

10.

start the service
