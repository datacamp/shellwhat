install:
	docker build -t shellwhat .

clean:
	find . \( -name \*.pyc -o -name \*.pyo -o -name __pycache__ \) -prune -exec rm -rf {} +
	rm -rf sqlwhat.egg-info

test: clean install
	docker run --rm shellwhat

dev: clean install
	docker run --rm -it -d --name oilc shellwhat /bin/bash
	@echo ''
	@echo 'to use with Osh AST Parser, use command below ---------------------'
	@echo 'export SHELLWHAT_PARSER="docker"'
	@echo 'to use without AST Parser, use command below ----------------------'
	@echo 'export SHELLWHAT_PARSER="0"'
