apt:
	sudo apt-get install -y upx-ucl

setup:
	pip install --upgrade pip setuptools wheel
	pip install -r requirements.txt
	python setup.py develop

clean:
	rm -f `find . -name \*.pyc`
	rm -rf `find . -name __pycache__`
	rm -rf build/ dist/
	rm -rf lib/lamemaker.egg-info

distclean: clean
	rm -rf ENV

uninstall:
	pip uninstall lamemaker
