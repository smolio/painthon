GCC=gcc
LD=ld
LIBS=

painthon: painthon.xml floodfill.so

painthon.xml: painthon.glade
	@gtk-builder-convert painthon.glade painthon.xml
	@cat painthon.xml | sed -e "s/buf\">/buf\">icons\//" > /tmp/painthon.xml
	@mv /tmp/painthon.xml painthon.xml
	@cat painthon.xml | sed -e "s/icon\">painthon.svg/icon\">pixmaps\/painthon.svg/" > /tmp/painthon.xml
	@mv /tmp/painthon.xml painthon.xml

floodfill.so: ./lib/c/floodfill.o
	$(LD) -shared -soname $@ -o ./lib/c/$@ -lc ./lib/c/floodfill.o

floodfill.o: ./lib/c/floodfill.c
	$(GCC) -fPIC $(LIBS) -o ./lib/c/floodfill.o -c ./lib/c/floodfill.c

clean:
	@rm -f painthon.xml ./lib/c/floodfill.o ./lib/c/floodfill.so
