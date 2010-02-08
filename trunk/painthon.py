#!/usr/bin/python
 
# Import packages
import pygtk
pygtk.require("2.0")
import gtk
import math
import cairo
from lib.misc.hsvgenerator import HSVGenerator
from lib.graphics.colorcell import ColorCell
from lib.graphics.fancycanvas import FancyCanvas
from lib.graphics.rgbacolor import RGBAColor
 

class Painthon():

   def __init__(self):
      '''Starting...'''
      builder = gtk.Builder()
      builder.add_from_file("painthon.xml")
      builder.connect_signals(self)

      # Set the first tool to use...
      self.current_tool = builder.get_object("btn-tool-free-select")
      self.current_tool.set_active(True)

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

      # Initialize canvas
      viewport = builder.get_object("viewport-for-canvas")
      self.canvas = FancyCanvas()
      viewport.add(self.canvas)

      # Show the window
      self.window.show_all()


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
         self.primary.set_color(c)
      elif event.button == 3:
         c.set_alpha(self.secondary.get_color().get_alpha())
         self.secondary.set_color(c)


   def change_tool_gui(self, newtool, data=None):
      if newtool.get_active():
          prevtool = self.current_tool
          if newtool != prevtool:
              self.current_tool = newtool
              prevtool.set_active(False)
              self.change_tool(newtool)

      else:
          if newtool == self.current_tool:
              newtool.set_active(True);


   def change_tool(self, tool):
      print("New tool selected: "+tool.get_name())
      # TODO: delete me
      w = self.canvas.get_width()
      h = self.canvas.get_height()
      if tool.get_name() == "btn-tool-draw-ellipse":
         w -= 10
         h -= 10
      if tool.get_name() == "btn-tool-draw-rounded-rectangle":
         w += 10
         h += 10
      self.canvas.set_size(max(w,10), max(h,10))


   def change_primary_alpha(self, slider):
      c = self.primary.get_color()
      print slider.get_value()
      value = slider.get_value()/100
      print value
      c.set_alpha(value)
      self.primary.set_color(c)


   def change_secondary_alpha(self, slider):
      c = self.secondary.get_color()
      value = slider.get_value()/100
      c.set_alpha(value)
      self.secondary.set_color(c)


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



if __name__ == "__main__":
   app = Painthon()

   gtk.main()
