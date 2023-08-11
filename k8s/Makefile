activate-virtualenv:
	poetry shell

install-dependency:
	poetry install

update-env-variable:
	set -a
	# use this to mean 'source .env'
	# ref:https://stackoverflow.com/questions/44052093/makefile-with-source-get-error-no-such-file-or-directory
	. .env
	set +a

checker:
	poetry run mypy ./src --check-untyped-defs

linter:
	poetry run black ./src --check
	poetry run ruff check ./src

formatter:
	poetry run black ./src -v
	poetry run ruff check ./src --fix
	poetry run isort ./src -v

test:
	poetry run pytest ./src/test

precommit:
	poetry run pre-commit run

start-k8s:
	minikube start --driver=docker

k8s-dashboard:
	minikube dashboard

docker-build:
	docker build -t localk8s .

docker-rm:
	docker rm $$(docker ps -aq -f "name=localk8s")

docker-run:
	make -k docker-rm
	docker run --name localk8s -p 8002:8002 localk8s

docker-exec:
	docker exec -it localk8s bash

docker-stop:
	docker stop  localk8s

get-pod:
	kubectl get pod 

get-service:
	kubectl get service

get-ingress:
	kubectl get ingress

get-deployment:
	kubectl get deployment

