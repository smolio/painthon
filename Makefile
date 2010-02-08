painthon: painthon.xml

painthon.xml: painthon.glade
	@gtk-builder-convert painthon.glade painthon.xml
	@cat painthon.xml | sed -e "s/buf\">/buf\">icons\//" > /tmp/painthon.xml
	@mv /tmp/painthon.xml painthon.xml
	@cat painthon.xml | sed -e "s/icon\">painthon.svg/icon\">pixmaps\/painthon.svg/" > /tmp/painthon.xml
	@mv /tmp/painthon.xml painthon.xml
