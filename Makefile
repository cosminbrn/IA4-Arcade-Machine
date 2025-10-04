.PHONY: run install uninstall

run:
	pipx uninstall rouge_tetris && cd src && pipx install -e . && rouge_tetris

install:
	cd src && pipx install -e .

uninstall:
	pipx uninstall rouge_tetris