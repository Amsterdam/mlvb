RM        := rm -rf
BUILDDIR  := ../docs

docs:
	npm run build
	$(RM) $(BUILDDIR)
	CP -a dist/. $(BUILDDIR)
