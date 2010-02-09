#!/usr/bin/python
 
# Import packages
import pygtk
pygtk.require("2.0")
import gtk
import gettext
import math
import cairo
import os
import sys

from lib.misc.hsvgenerator import HSVGenerator
from lib.graphics.colorcell import ColorCell
from lib.graphics.fancycanvas import FancyCanvas
from lib.graphics.rgbacolor import RGBAColor
from lib.io.generic import ImageFile
from lib.tools.figures import *
from lib.tools.generic import *

_ = gettext.gettext
 
class Painthon():

   def __init__(self, path, image_filename=None):
      builder = gtk.Builder()
      builder.add_from_file("painthon.xml")

      # Get the window properly
      self.window = builder.get_object("main-window")

      # Reader and Writer Tools
      self.READWRITE = ImageFile()

      # Initialize canvas
      viewport = builder.get_object("viewport-for-canvas")
      self.CANVAS = FancyCanvas()
      viewport.add(self.CANVAS)

      # Load image information
      self.is_modified = False
      if image_filename != None:
         info = self.READWRITE.read(os.path.abspath(image_filename))
         self.__set_current_info(info)
      else:
         self.filename = _("unknown")
         self.path = path
         self.update_title()


      # Defining tools
      self.TOOLS = {"btn-tool-draw-rectangle" : RectangleTool(self.CANVAS),
                    "btn-tool-draw-rounded-rectangle" : RoundedRectangleTool(self.CANVAS),
                    "btn-tool-draw-ellipse"   : EllipseTool(self.CANVAS) }

      # Set the first tool to use...
      # TODO: select the proper default tool
      #self.active_tool_button = builder.get_object("btn-tool-free-select")
      self.active_tool_button = builder.get_object("btn-tool-draw-rectangle")
      self.active_tool_button.set_active(True)
      self.CANVAS.set_active_tool(self.TOOLS[self.active_tool_button.get_name()])

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
      self.MAX_ALPHA_1 = a1.get_value()
      a2 = builder.get_object("secondary-color-alpha")
      a2.set_value(a2.get_value())
      self.MAX_ALPHA_2 = a2.get_value()

      # Connecting signals properly...
      builder.connect_signals(self)

      # Show the window
      self.window.show_all()


   def update_title(self):
      if self.is_modified:
         self.window.set_title("*" + self.filename + " - Painthon")
      else:
         self.window.set_title(self.filename + " - Painthon")


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
      value = slider.get_value()/self.MAX_ALPHA_1
      c.set_alpha(value)
      self.__set_primary_color_to(c)


   def change_secondary_alpha(self, slider):
      c = self.secondary.get_color()
      value = slider.get_value()/self.MAX_ALPHA_2
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
      info = self.READWRITE.open(self.path + os.sep + self.filename)
      self.__set_current_info(info)


   def save(self, widget):
      canonical_filename = self.READWRITE.save(self.CANVAS.get_image(), self.path, self.filename)
      self.__fix_image_info(canonical_filename)


   def save_as(self, widget):
      canonical_filename = self.READWRITE.save_as(self.CANVAS.get_image(), self.path, self.filename)
      self.__fix_image_info(canonical_filename)


   def __set_current_info(self, image_info):
      canonical_filename = image_info[0]
      self.CANVAS.set_image(image_info[1])
      self.CANVAS.set_image_type(image_info[2])
      self.__fix_image_info(canonical_filename)


   def __fix_image_info(self, canonical_filename):
      self.filename = os.path.basename(canonical_filename)
      self.path = os.path.dirname(canonical_filename)
      self.update_title()


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
   filename = None
   if len(sys.argv) == 2:
      filename = sys.argv[1]

   app = Painthon(os.environ['HOME'], filename)

   gtk.main()
