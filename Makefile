install:
	docker build -t shellwhat .

clean:
	find . \( -name \*.pyc -o -name \*.pyo -o -name __pycache__ \) -prune -exec rm -rf {} +
	rm -rf shellwhat.egg-info

test: clean install
	docker run --rm shellwhat

run:
	docker run --rm -it -d --name oilc shellwhat /bin/bash

dev: clean install run
