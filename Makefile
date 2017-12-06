.PHONY: pep8 heroku_push web bot build pull perm dev_info base migrate_dev

base_tag = austinpray/kizuna/base
bot_tag = austinpray/kizuna/bot
web_tag = austinpray/kizuna/web

registry_base_url = registry.heroku.com/kizunaai

registry_base_tag = $(registry_base_url)/base
registry_bot_tag = $(registry_base_url)/bot
registry_web_tag = $(registry_base_url)/web

build: bot web

pep8:
	docker run --rm -v $(shell pwd):/code omercnet/pycodestyle --show-source /code

heroku_push:
	docker tag $(base_tag) $(registry_base_tag)
	docker tag $(bot_tag) $(registry_bot_tag)
	docker tag $(web_tag) $(registry_web_tag)
	docker push $(registry_base_tag)
	docker push $(registry_bot_tag)
	docker push $(registry_web_tag)

pull:
	docker pull $(registry_base_tag)
	docker pull $(registry_bot_tag)
	docker pull $(registry_web_tag)
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
	bin/generate-dev-info.py --revision $(shell git rev-parse HEAD) > .dev-info.json

dev:
	concurrently --kill-others --names "BOT,WEB" \
		"nodemon -e 'py' --watch bot.py --watch kizuna/ --exec docker-compose restart bot" \
		"nodemon -e 'py' --watch web.py --watch kizuna_web/ --exec docker-compose restart web"

migrate_dev:
	docker-compose run bot alembic upgrade head
