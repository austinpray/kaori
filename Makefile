.PHONY: build publish test test-all test-% clean

build:
	python setup.py sdist bdist_wheel

publish: build
	twine upload dist/*

test:
	${MAKE} test-3.7

test-all:
	${MAKE} test-3.7
	${MAKE} test-3.6
	${MAKE} test-3.5


ifeq ($(FAST),true)
DOCKER_VOLUMES =  -v $(shell pwd):/app
else
DOCKER_VOLUMES =  -v $(shell pwd):/app
DOCKER_VOLUMES += -v /app/.eggs
DOCKER_VOLUMES += -v /app/.pytest_cache
DOCKER_VOLUMES += -v /app/slacktools.egg-info
endif

test-%:
	docker run --rm ${DOCKER_VOLUMES} -w /app python:$(@:test-%=%) python setup.py test

clean:
	git clean -fdx -e *.iml -e .idea
