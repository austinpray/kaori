.PHONY: pep8

pep8:
	docker run --rm -v $(shell pwd):/code omercnet/pycodestyle --show-source /code
