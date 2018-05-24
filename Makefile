test: clean
	rm -rf shellwhat/tests/__pycache__
	docker build -t shellwhat .
	docker run --rm shellwhat

clean:
	find . \( -name \*.pyc -o -name \*.pyo -o -name __pycache__ \) -prune -exec rm -rf {} +
	rm -rf sqlwhat.egg-info

dev:
	docker build -t shellwhat .
	docker rm -f oilc
	docker run --rm -it -d --name oilc shellwhat /bin/bash
	@echo ''
	@echo 'to use with Osh AST Parser, use command below ---------------------'
	@echo 'export SHELLWHAT_PARSER="docker"'
	@echo 'to use without AST Parser, use command below ----------------------'
	@echo 'export SHELLWHAT_PARSER="0"'
