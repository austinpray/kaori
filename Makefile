.PHONY: pep8 heroku_push web bot build pull perm

registry_base = registry.heroku.com/kizunaai
bot_tag = $(registry_base)/bot
web_tag = $(registry_base)/web

pep8:
	docker run --rm -v $(shell pwd):/code omercnet/pycodestyle --show-source /code

heroku_push:
	docker push $(bot_tag)
	docker push $(web_tag)

pull:
	docker pull $(bot_tag)
	docker pull $(web_tag)

web:
	docker run -it --rm --name build-web-assets -v $(shell pwd):/kizuna -w /kizuna node:9 npm run build
	docker build \
		--cache-from $(web_tag) \
		-t $(web_tag) \
		--build-arg entry='gunicorn -w 4 -b 0.0.0.0:$PORT web:app' \
		.

bot:
	docker build \
		--cache-from $(bot_tag) \
		-t $(bot_tag) \
		--build-arg entry='python -u ./bot.py' \
		.

build: bot web

perm:
	sudo chown -R $(shell whoami):$(shell whoami) .
