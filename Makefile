SHELL := /bin/zsh

install:
	pip install -r requirements.txt

lint:
	python =pylint pytherman.py core components systems

isort:
	isort -rc -ac .

run:
	python pytherman.py