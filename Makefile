.PHONY: build api worker web
.PHONY: clean ci_%

build: api worker web

api: image_api

worker: image_worker

web: image_web

clean: perms docker_clean
	git clean -fdx -e .idea -e .env

ci_%:
	$(MAKE) registry_pull_$(*)
	$(MAKE) image_$(*)
	$(MAKE) registry_push_$(*)

TRAVIS_COMMIT ?= $(shell git rev-parse HEAD)-WIP

local_prefix ?= austinpray/kizuna
registry_prefix ?= us.gcr.io/kizuna-188702

DRUN = docker run -it --rm -v $(shell pwd):/kizuna -w /kizuna
NODE = $(DRUN) --name kizuna-node-$$(uuidgen) node:10
PYTHON = $(DRUN) --name kizuna-py-$$(uuidgen) python:3.6
KIZ = $(DRUN) --name kizuna-$$(uuidgen) $(local_prefix)/base

.PHONY: test dev_info

test:
	$(KIZ) pytest

# make a dev-info file so kizuna knows what commit she's on
dev_info:
	bin/generate-dev-info.py --revision $(TRAVIS_COMMIT) > .dev-info.json


# push all the images to gcloud registry
.PHONY: registry_pull_% registry_pull image_% registry_push_% kube_deploy_% docker_clean

# pull images from registry prolly for caching reasons
registry_pull_%:
	docker pull $(registry_prefix)/$(*)
	docker tag $(registry_prefix)/$(*) $(local_prefix)/$(*)

registry_pull: registry_pull_base registry_pull_api registry_pull_web registry_pull_worker

DOCKER_BUILD =  docker build
ifeq ($(KIZ_CACHE),true)
DOCKER_BUILD += --cache-from $(registry_prefix)/{{T}}
endif
DOCKER_BUILD += --file docker/{{T}}/Dockerfile
DOCKER_BUILD += -t $(local_prefix)/{{T}}
DOCKER_BUILD += .

.PHONY: image_base image_% image_web image_tag_% image_tag

image_base:
	$(subst {{T}},base,$(DOCKER_BUILD))

image_web: image_base static/dist
	$(subst {{T}},web,$(DOCKER_BUILD))

image_%: image_base
	$(subst {{T}},$(*),$(DOCKER_BUILD))

image_tag_%:
	docker tag $(local_prefix)/$(*) $(registry_prefix)/$(*):$(TRAVIS_COMMIT)
	docker tag $(local_prefix)/$(*) $(registry_prefix)/$(*):latest

image_tag: image_tag_api image_tag_web image_tag_worker

.PHONY: registry_push_% registry_push

registry_push_%: image_tag_%
	docker push $(registry_prefix)/$(*):$(TRAVIS_COMMIT)
	docker push $(registry_prefix)/$(*):latest

registry_push: registry_push_api registry_push_web registry_push_worker

.PHONY: kube_deploy_% kube_deploy

kube_deploy_%: registry_push_%
	kubectl set image deployment/$(*) api=$(registry_prefix)/$(*)

kube_deploy: kube_deploy_api kube_deploy_web kube_deploy_worker

.PHONY: docker_clean

docker_clean:
	docker rmi -f $(local_prefix)/api
	docker rmi -f $(local_prefix)/base
	docker rmi -f $(local_prefix)/web
	docker rmi -f $(local_prefix)/worker

	docker rmi -f $(registry_prefix)/api
	docker rmi -f $(registry_prefix)/base
	docker rmi -f $(registry_prefix)/web
	docker rmi -f $(registry_prefix)/worker

# assets

.PHONY: assets-watch assets-dev

node_modules: package-lock.json
	${NODE} npm ci

static/dist: node_modules webpack.config.js src/kizuna/web/js
	${NODE} npm run build -- -p

assets-watch: node_modules
	${NODE} npm run build -- -d --watch

assets-dev:
	${NODE} bash

# dev commands
## watch for file changes and restart accordingly
.PHONY: repl ngrok pep8 autopep8 perms dev dev_worker migrate_dev

repl:
	$(KIZ) python

ngrok:
	ngrok http -subdomain=kizuna 8001

# check the project for pep8 compliance
pep8:
	docker run --rm -v $(shell pwd):/code omercnet/pycodestyle --show-source /code/src

autopep8:
	find ./src -name '*.py' | xargs autopep8 --in-place --aggressive --aggressive


# docker permissions helper
perms:
	sudo chown -R $(shell whoami):$(shell whoami) .

dev:
	nodemon -e 'py' --exec docker-compose restart api web worker

dev_worker:
	nodemon -e 'py' --exec docker-compose restart worker

## run dev migrations
migrate_dev:
	docker-compose run api alembic upgrade head

## slacktools
.PHONY: pull-slacktools push-slacktools

pull-slacktools:
	git subtree pull --prefix vendor/python-slacktools python-slacktools dev --squash

push-slacktools:
	git subtree push --prefix vendor/python-slacktools python-slacktools dev
