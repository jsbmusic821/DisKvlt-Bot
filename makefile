make: all

all:
	apt install python3-pip py3-setuptools
	pip3.6 install --user wheel lyricfetcher discord bs4 asyncio translate html5lib
