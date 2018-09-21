.PHONY: build clean

# build everything
build: api worker web

clean: assets-clean

# simulate CI environment
TRAVIS_COMMIT ?= $(shell git rev-parse HEAD)-ts$(date +"%T")

# remote registry prefix for pushing to gcloud
local_prefix ?= austinpray/kizuna
registry_prefix ?= us.gcr.io/kizuna-188702

DRUN = docker run -it --rm -v $(shell pwd):/kizuna -w /kizuna
NODE = $(DRUN) --name kizuna-node-$$(uuidgen) node:10
PYTHON = $(DRUN) --name kizuna-py-$$(uuidgen) python:3.6
KIZ = $(DRUN) --name kizuna-$$(uuidgen) $(local_prefix)/base

.PHONY: test

test:
	$(KIZ) pytest

# make a dev-info file so kizuna knows what commit she's on
dev_info:
	bin/generate-dev-info.py --revision $(TRAVIS_COMMIT) > .dev-info.json


# push all the images to gcloud registry
.PHONY: registry_push_%

registry_push_%:
	docker tag $(local_prefix)/% $(registry_prefix)/%:$(TRAVIS_COMMIT)
	docker tag $(local_prefix)/% $(registry_prefix)/%:latest
	docker push $(registry_prefix)/%:$(TRAVIS_COMMIT)
	docker push $(registry_prefix)/%:latest


registry_push: \
	registry_push_base \
	registry_push_api \
	registry_push_web \
	registry_push_worker

# release the current commit to kube
kube_deploy: registry_push
	kubectl set image deployment/api api=$(registry_api_tag_commit)
	kubectl set image deployment/web web=$(registry_web_tag_commit)
	kubectl set image deployment/worker worker=$(registry_worker_tag_commit)

# pull images from registry prolly for caching reasons
pull:
	gcloud docker -- pull $(registry_base_tag)
	gcloud docker -- pull $(registry_api_tag)
	gcloud docker -- pull $(registry_web_tag)
	gcloud docker -- pull $(registry_worker_tag)
	docker tag $(registry_base_tag) $(base_tag)
	docker tag $(registry_api_tag) $(api_tag)
	docker tag $(registry_web_tag) $(web_tag)
	docker tag $(registry_worker_tag) $(worker_tag)

docker_clean:
	docker rmi -f $(local_prefix)/api
	docker rmi -f $(local_prefix)/web
	docker rmi -f $(local_prefix)/base
	docker rmi -f $(local_prefix)/worker
	docker rmi -f $(registry_prefix)/api
	docker rmi -f $(registry_prefix)/web
	docker rmi -f $(registry_prefix)/base
	docker rmi -f $(registry_prefix)/worker

# image building
.PHONY: image_%

image_%:
	basename = $(@:image_%=%)
	docker build \
		--file docker/$% \
		--cache-from $(registry_prefix)/$(basename) \
		-t $(local_prefix)/$(basename) \
		.

api: base
	docker build \
		--file docker/api \
		--cache-from $(api_tag) \
		-t $(api_tag) \
		.

node_modules: package-lock.json
	${NODE} npm ci

static/dist: node_modules webpack.config.js src/web/js
	${NODE} npm run build -- -p

assets-watch: node_modules
	${NODE} npm run build -- -d --watch

assets-dev:
	${NODE} bash

assets-clean:
	${NODE} rm -rf node_modules static/dist


web: base
	${MAKE} assets
	docker build \
		--file docker/web \
		--cache-from $(web_tag) \
		-t $(web_tag) \
		.

worker: base
	docker build \
		--file docker/worker \
		--cache-from $(worker_tag) \
		-t $(worker_tag) \
		.

# dev commands
## watch for file changes and restart accordingly
.PHONY: repl ngrok pep8 autopep8 perm dev dev_worker migrate_dev

repl:
	$(KIZ) python

ngrok:
	ngrok http -subdomain=kizuna 8001

# check the project for pep8 compliance
pep8:
	docker run --rm -v $(shell pwd):/code omercnet/pycodestyle --show-source /code

autopep8:
	find . -name '*.py' | xargs autopep8 --in-place --aggressive --aggressive


# docker permissions helper
perm:
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
