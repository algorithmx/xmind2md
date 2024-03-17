clean:
	rm -rf  __pycache__/  */__pycache__/  *.egg-info 


init:
	rm -rf .env
	rm -rf  __pycache__/  */__pycache__/  *.egg-info 
	./init.sh

setup:
	pip install -e .
