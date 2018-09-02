.PHONY: kub_deploy web api build pull perm dev_info base migrate_dev
.PHONY: test ngrok repl
.PHONY: dev dev_worker
.PHONY: pep8 autopep8
.PHONY: \
	registry_push \
	registry_push_base \
	registry_push_api \
	registry_push_web \
	registry_push_worker

# simulate CI environment
TRAVIS_COMMIT ?= $(shell git rev-parse HEAD)-ts$(date +"%T")

NODE = docker run -it --rm --name kizuna-node-$$(uuidgen) -v $(shell pwd):/kizuna -w /kizuna node:10

# tags used locally
base_tag = austinpray/kizuna/base

api_tag = austinpray/kizuna/api
web_tag = austinpray/kizuna/web
worker_tag = austinpray/kizuna/worker

# remote registry prefix for pushing to gcloud
registry_prefix = us.gcr.io/kizuna-188702

# base tags for different images in project
registry_base_tag = $(registry_prefix)/base

registry_api_tag = $(registry_prefix)/api
registry_web_tag = $(registry_prefix)/web
registry_worker_tag = $(registry_prefix)/worker

# commit level tag
registry_base_tag_commit = $(registry_base_tag):$(TRAVIS_COMMIT)

registry_api_tag_commit = $(registry_api_tag):$(TRAVIS_COMMIT)
registry_web_tag_commit = $(registry_web_tag):$(TRAVIS_COMMIT)
registry_worker_tag_commit = $(registry_worker_tag):$(TRAVIS_COMMIT)

# latest tags
registry_base_tag_latest = $(registry_base_tag):latest

registry_api_tag_latest = $(registry_api_tag):latest
registry_web_tag_latest = $(registry_web_tag):latest
registry_worker_tag_latest = $(registry_worker_tag):latest

# build everything
build: dev_info api worker web

# check the project for pep8 compliance
pep8:
	docker run --rm -v $(shell pwd):/code omercnet/pycodestyle --show-source /code

autopep8:
	find . -name '*.py' | xargs autopep8 --in-place --aggressive --aggressive

test:
	docker run --rm -v $(shell pwd):/kizuna $(base_tag) pytest

repl:
	docker run --rm -it -v $(shell pwd):/kizuna $(base_tag) python

ngrok:
	ngrok http -subdomain=kizuna 8001

# make a dev-info file so kizuna knows what commit she's on
dev_info:
	bin/generate-dev-info.py --revision $(TRAVIS_COMMIT) > .dev-info.json

# push all the images to gcloud registry
registry_push_base:
	docker tag $(base_tag) $(registry_base_tag_commit)
	docker tag $(base_tag) $(registry_base_tag_latest)
	gcloud docker -- push $(registry_base_tag_commit)
	gcloud docker -- push $(registry_base_tag_latest)

registry_push_api:
	docker tag $(api_tag) $(registry_api_tag_commit)
	docker tag $(api_tag) $(registry_api_tag_latest)
	gcloud docker -- push $(registry_api_tag_commit)
	gcloud docker -- push $(registry_api_tag_latest)

registry_push_web:
	docker tag $(web_tag) $(registry_web_tag_commit)
	docker tag $(web_tag) $(registry_web_tag_latest)
	gcloud docker -- push $(registry_web_tag_commit)
	gcloud docker -- push $(registry_web_tag_latest)

registry_push_worker:
	docker tag $(worker_tag) $(registry_worker_tag_commit)
	docker tag $(worker_tag) $(registry_worker_tag_latest)
	gcloud docker -- push $(registry_worker_tag_commit)
	gcloud docker -- push $(registry_worker_tag_latest)


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

# image building
base:
	docker build \
		--file Dockerfile.base \
		--cache-from $(base_tag) \
		-t $(base_tag) \
		.

api: base
	docker build \
		--file Dockerfile.api \
		--cache-from $(api_tag) \
		-t $(api_tag) \
		.

node_modules: package-lock.json
	${NODE} npm ci

assets: node_modules
	${NODE} npm run build -- -p

assets-watch: node_modules
	${NODE} npm run build -- -d --watch

assets-dev:
	${NODE} bash

assets-clean:
	${NODE} rm -rf node_modules


web: api
	${MAKE} assets
	docker build \
		--file Dockerfile.web \
		--cache-from $(web_tag) \
		-t $(web_tag) \
		.

worker: base
	docker build \
		--file Dockerfile.worker \
		--cache-from $(worker_tag) \
		-t $(worker_tag) \
		.

# docker permissions helper
perm:
	sudo chown -R $(shell whoami):$(shell whoami) .

# dev commands
## watch for file changes and restart accordingly
dev:
	nodemon -e 'py' --exec docker-compose restart api web worker

dev_worker:
	nodemon -e 'py' --exec docker-compose restart worker

## run dev migrations
migrate_dev:
	docker-compose run api alembic upgrade head
