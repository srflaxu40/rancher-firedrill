#Most vars can be ovewritten with ENV vars (like Jenkins)
PROJECT_NAME ?= firedrill 
ENVIRONMENT ?= develop

rancher_deploy:
	rancher-compose --verbose \
	-f docker-compose-rancher.yml \
	-p firedrill \
	up \
	--pull \
	--force-upgrade \
	--confirm-upgrade \
	-d

build:
	docker build --no-cache \
	-t firedrill:latest .
