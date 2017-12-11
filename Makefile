.PHONY: kub_deploy pep8 registry_push web bot build pull perm dev_info base migrate_dev

base_tag = austinpray/kizuna/base
bot_tag = austinpray/kizuna/bot
web_tag = austinpray/kizuna/web

registry_base_url = registry.heroku.com/kizunaai
registry_base_url = us.gcr.io/kizuna-188702

TRAVIS_COMMIT ?= $(shell git rev-parse HEAD)

registry_base_tag = $(registry_base_url)/base
registry_bot_tag = $(registry_base_url)/bot
registry_web_tag = $(registry_base_url)/web

registry_base_tag_commit = $(registry_base_tag):$(TRAVIS_COMMIT)
registry_bot_tag_commit = $(registry_bot_tag):$(TRAVIS_COMMIT)
registry_web_tag_commit = $(registry_web_tag):$(TRAVIS_COMMIT)

registry_base_tag_latest = $(registry_base_tag):latest
registry_bot_tag_latest = $(registry_bot_tag):latest
registry_web_tag_latest = $(registry_web_tag):latest

build: dev_info bot web

pep8:
	docker run --rm -v $(shell pwd):/code omercnet/pycodestyle --show-source /code

registry_push:
	docker tag $(base_tag) $(registry_base_tag_commit)
	docker tag $(bot_tag) $(registry_bot_tag_commit)
	docker tag $(web_tag) $(registry_web_tag_commit)
	gcloud docker -- push $(registry_base_tag_commit)
	gcloud docker -- push $(registry_bot_tag_commit)
	gcloud docker -- push $(registry_web_tag_commit)

kube_deploy: registry_push
	kubectl set image deployment/bot bot=$(registry_bot_tag_commit)
	kubectl set image deployment/web web=$(registry_web_tag_commit)

pull:
	gcloud docker -- pull $(registry_base_tag)
	gcloud docker -- pull $(registry_bot_tag)
	gcloud docker -- pull $(registry_web_tag)
	docker tag $(registry_base_tag) $(base_tag)
	docker tag $(registry_bot_tag) $(bot_tag)
	docker tag $(registry_web_tag) $(web_tag)

base:
	docker build \
		--file Dockerfile.base \
		--cache-from $(base_tag) \
		-t $(base_tag) \
		.

bot: base
	docker build \
		--file Dockerfile.bot \
		--cache-from $(bot_tag) \
		-t $(bot_tag) \
		.

web: bot
	docker run -it --rm --name build-web-assets -v $(shell pwd):/kizuna -w /kizuna node:9 npm run build
	docker build \
		--file Dockerfile.web \
		--cache-from $(web_tag) \
		-t $(web_tag) \
		.

perm:
	sudo chown -R $(shell whoami):$(shell whoami) .

dev_info:
	bin/generate-dev-info.py --revision $(TRAVIS_COMMIT) > .dev-info.json

dev:
	nodemon -e 'py' --exec docker-compose restart bot web

migrate_dev:
	docker-compose run bot alembic upgrade head
