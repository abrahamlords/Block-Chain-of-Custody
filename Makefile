all:	block.py
	cp block.py bchoc
	chmod +x bchoc

clean:
	($RM) bchoc

