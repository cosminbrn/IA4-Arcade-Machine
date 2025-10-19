.PHONY: run install uninstall

run:
	pipx uninstall interface && cd src && pipx install -e . && interface

install:
	cd src && pipx install -e .

uninstall:
	pipx uninstall interface