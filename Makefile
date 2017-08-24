test:
	rm -rf shellwhat/tests/__pycache__
	docker build -t shellwhat .
	docker run --rm shellwhat
