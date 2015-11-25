#
# Makefile for HSR-LateX-Template
#

BASENAME = main
MAIN_TEX = $(BASENAME).tex
BULD_CMD = ./bin/latexmk.pl -pdf $(MAIN_TEX)
DEST_NAME = Thesis

# Don't ask me why.
all: build
	@@mv $(BASENAME).pdf $(DEST_NAME).pdf

build:
	@@$(BULD_CMD)

live:
	@@$(BULD_CMD) --pvc

clean-auxilary:
	-rm $(BASENAME).aux $(BASENAME).glo $(BASENAME).idx $(BASENAME).ist
	-rm $(BASENAME).lof $(BASENAME).out $(BASENAME).toc
	-rm $(BASENAME).glg $(BASENAME).gls *.log $(BASENAME).bbl
	-rm $(BASENAME).blg $(BASENAME).fdb_latexmk $(BASENAME).fls $(BASENAME).ilg
	-rm $(BASENAME).ind $(BASENAME).ind $(BASENAME).ilg $(BASENAME).fls

clean: clean-auxilary
	-rm $(BASENAME).pdf
