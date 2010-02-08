#!/usr/bin/python
 
# Import packages
import pygtk
pygtk.require("2.0")
import gtk
import gettext
import math
import cairo
from lib.misc.hsvgenerator import HSVGenerator
from lib.graphics.colorcell import ColorCell
from lib.graphics.fancycanvas import FancyCanvas
from lib.graphics.rgbacolor import RGBAColor
from lib.tools.figures import *
from lib.tools.generic import *

_ = gettext.gettext
 

class Painthon():

   def __init__(self, image_filename=None):
      '''Starting...'''
      builder = gtk.Builder()
      builder.add_from_file("painthon.xml")
      builder.connect_signals(self)

      # Initialize canvas
      # TODO: pass image reference...
      viewport = builder.get_object("viewport-for-canvas")
      self.CANVAS = FancyCanvas()
      viewport.add(self.CANVAS)

      # Defining tools
      self.TOOLS = {"btn-tool-draw-rectangle" : RectangleTool(self.CANVAS),
                    "btn-tool-draw-ellipse"   : EllipseTool(self.CANVAS) }

      # Set the first tool to use...
      # TODO: This is the one ;-)
      #self.active_tool_button = builder.get_object("btn-tool-free-select")
      self.active_tool_button = builder.get_object("btn-tool-draw-rectangle")
      self.active_tool_button.set_active(True)
      self.CANVAS.set_active_tool(self.TOOLS[self.active_tool_button.get_name()])

      # Get the window properly
      self.window = builder.get_object("main-window")

      # Get the toolbar and set it not to show text
      self.toolbar = builder.get_object("toolbar")
      self.toolbar.set_style(gtk.TOOLBAR_ICONS)

      # Initialize palette
      self.__init_colors(builder.get_object("colors-grid"))

      # Initialize working colors
      self.primary = ColorCell(0, 0, 0)
      self.primary.connect("button-release-event", self.color_changed)
      primary_frame = builder.get_object("primary-color")
      primary_frame.add(self.primary)
      self.secondary = ColorCell(1, 1, 1)
      self.secondary.connect("button-release-event", self.color_changed)
      secondary_frame = builder.get_object("secondary-color")
      secondary_frame.add(self.secondary)

      # Fix alpha sliders
      a1 = builder.get_object("primary-color-alpha")
      a1.set_value(a1.get_value())
      a2 = builder.get_object("secondary-color-alpha")
      a2.set_value(a2.get_value())

      # Setting filename
      self.filename = _("unknown")
      self.update_title()

      # Show the window
      self.window.show_all()


   def update_title(self):
      self.window.set_title("*" + self.filename + " - Painthon")


   def __init_colors(self, colorsgrid):
      colors = colorsgrid.get_children()
      rows = colorsgrid.get_property("n-rows")
      columns = colorsgrid.get_property("n-columns")

      # Color[0][0]
      color_frame = colors[0]
      colorcell = ColorCell(0, 0, 0)
      colorcell.connect("button-release-event", self.color_changed)
      color_frame.add(colorcell)
      # Color[0][1]
      color_frame = colors[columns]
      colorcell = ColorCell(1, 1, 1)
      colorcell.connect("button-release-event", self.color_changed)
      color_frame.add(colorcell)

      # Color[1][0]
      color_frame = colors[1]
      colorcell = ColorCell(0.33, 0.33, 0.33)
      colorcell.connect("button-release-event", self.color_changed)
      color_frame.add(colorcell)
      # Color[1][1]
      color_frame = colors[columns + 1]
      colorcell = ColorCell(0.66, 0.66, 0.66)
      colorcell.connect("button-release-event", self.color_changed)
      color_frame.add(colorcell)

      hsv = HSVGenerator()

      # The other colors
      for i in range(rows):
         for j in range(2, columns):
            # Each cell is: frame{ eventbox{label} }
            color_frame = colors[i*columns + j]
            color = hsv.get_hsv_color(360*(j-2)/(columns-2), 1.0-0.7*i, 1.0)
            colorcell = ColorCell()
            colorcell.connect("button-release-event", self.color_changed)
            colorcell.set_color(RGBAColor.create_from_gtk_color(color))
            color_frame.add(colorcell)


   def quit(self, window, data=None):
      gtk.main_quit()


   def color_changed(self, widget, event):
      c = widget.get_color()
      if event.button == 1:
         c.set_alpha(self.primary.get_color().get_alpha())
         self.__set_primary_color_to(c)
      elif event.button == 3:
         c.set_alpha(self.secondary.get_color().get_alpha())
         self.__set_secondary_color_to(c)


   def change_tool_gui(self, newtool, data=None):
      if newtool.get_active():
          prevtool = self.active_tool_button
          if newtool != prevtool:
              self.active_tool_button = newtool
              prevtool.set_active(False)
              self.change_tool(newtool)

      else:
          if newtool == self.active_tool_button:
              newtool.set_active(True);


   def change_tool(self, tool):
      self.CANVAS.set_active_tool(self.TOOLS[tool.get_name()])


   def change_primary_alpha(self, slider):
      c = self.primary.get_color()
      #TODO: delete me
      #print slider.get_value()
      value = slider.get_value()/100
      #TODO: delete me
      #print value
      c.set_alpha(value)
      self.__set_primary_color_to(c)


   def change_secondary_alpha(self, slider):
      c = self.secondary.get_color()
      value = slider.get_value()/100
      c.set_alpha(value)
      self.__set_secondary_color_to(c)


   def __set_primary_color_to(self, c):
      self.primary.set_color(c)
      for tool in self.TOOLS.values():
         tool.set_primary_color(c)


   def __set_secondary_color_to(self, c):
      self.secondary.set_color(c)
      for tool in self.TOOLS.values():
         tool.set_secondary_color(c)


   def new(self, widget):
      print widget.get_name()


   def open(self, widget):
      print widget.get_name()


   def save(self, widget):
      print widget.get_name()


   def save_as(self, widget):
      print widget.get_name()


   def cut(self, widget):
      print widget.get_name()


   def copy(self, widget):
      print widget.get_name()


   def paste(self, widget):
      print widget.get_name()


   def redo(self, widget):
      print widget.get_name()


   def undo(self, widget):
      print widget.get_name()



if __name__ == "__main__":
   app = Painthon()

   gtk.main()
