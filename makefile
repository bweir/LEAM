setup:
	sudo apt-get install -y upx-ucl
	pip install -r requirements.txt
	python setup.py develop

clean:
	rm -f `find lame/ -name \*.pyc`
	rm -f `find lamemaker/ -name \*.pyc`
	rm -rf build/ dist/
	rm -rf lamemaker.egg-info

distclean: clean
	rm -rf ENV
