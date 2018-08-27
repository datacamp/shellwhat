clean:
	find . \( -name \*.pyc -o -name \*.pyo -o -name __pycache__ \) -prune -exec rm -rf {} +
	rm -rf shellwhat.egg-info

build_docker:
	docker build -t shellwhat .

test: build_docker
	docker run --rm -it -d --name oilc shellwhat /bin/bash
	pytest --cov=shellwhat
	codecov
	docker stop oilc
