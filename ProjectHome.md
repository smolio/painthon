# Description #

This program mimics first versions of Microsoft Paint (before Windows 7) and extends its functionalities:

  * Alpha channel
  * Antialiased shapes and lines
  * More than three undos ;-)
  * Gradient fills
  * ...

## Current status ##

The project is in a very incipient state. I started the project to get some fun, and its code is dirty. Right now, I'm working on the Cairo (vector graphics) canvas to mimic raster graphics and on code refactoring.

I hope I'll have an 1.0 beta version soon.

# Technical info #

## Brief introduction ##

Painthon is written in Python using:

  * GTK+ (pygtk)
  * Cairo (pycairo)

## On icons... ##

Main toolbar icons are from gnome stock icons. Special thanks to OpenOffice.org team and GIMP, because tool icons are from their projects.

# Screenshots #

## First iteration screenshots ##

**Edit:** I've deleted these first screenshots, because they were not "real" (canvas contents were drawn programatically, not by the user using his mouse).

## Rectangle and Ellipse Tools working properly ##

![http://painthon.googlecode.com/svn/screenshots/painthon-03.png](http://painthon.googlecode.com/svn/screenshots/painthon-03.png)

_Example of rectangles and ellipses drawn using mouse events._

## Pencil, eraser and paintbrush working properly too! ##

![http://painthon.googlecode.com/svn/screenshots/painthon-04.png](http://painthon.googlecode.com/svn/screenshots/painthon-04.png)

_Finally, free drawing tools work. Some letters written using the paintbrush._