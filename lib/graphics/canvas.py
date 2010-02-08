import cairo
import gtk
import math
from lib.tools.generic import *

class Canvas(gtk.DrawingArea):
   active_tool = None
   drawing = False

   def __init__(self):
      # Initializing superclass
      super(Canvas, self).__init__()

      # Registering events
      #self.add_events(gtk.gdk.BUTTON_MOTION_MASK | gtk.gdk.BUTTON_PRESS | gtk.gdk.BUTTON_RELEASE)
      self.add_events(gtk.gdk.BUTTON_PRESS_MASK | gtk.gdk.BUTTON_RELEASE_MASK | gtk.gdk.BUTTON1_MOTION_MASK | gtk.gdk.DRAG_MOTION)
      self.connect("button-press-event", self.button_pressed)
      self.connect("button-release-event", self.button_released)
      self.connect("motion-notify-event", self.drag_event)
      self.connect("expose-event", self.expose)

      self.set_size(400, 300)


   def reset(self, context):
      # Clipping to draw area
      context.reset_clip()
      context.rectangle(0, 0, self.width, self.height)
      context.clip()


   def set_size(self, width, height):
      self.width = max(width, 1)
      self.height = max(height, 1)
      self.set_size_request(self.width, self.height)


   def get_width(self):
      return self.width


   def get_height(self):
      return self.height


   def expose(self, widget, event):
      context = widget.window.cairo_create()

      # Clipping area
      self.reset(context)

      # Drawing the background
      self.__draw_background(context)

      # Draw the result
      self.draw(context)
      if self.drawing:
         self.active_tool.draw(context)


   def button_pressed(self, widget, event):
      self.drawing = True
      self.active_tool.begin(event.x, event.y)


   def button_released(self, widget, event):
      self.drawing = False
      self.active_tool.end(event.x, event.y)


   def draw(self, context):

      # Painting circle
      context.arc(50, 50, 300, 0, 2.0 * math.pi)
      context.set_source_rgb(1, 0, 0)
      context.fill()

      # Make the circle look glossy
      context.arc(50, 50, 300, 0, 2.0 * math.pi)
      context.clip()
      context.arc(50, -800, 900, 0, 2.0 * math.pi)
      lg = cairo.LinearGradient(0, 0, 0, 400)
      lg.add_color_stop_rgba(0, 1, 1, 1, 0.9)
      lg.add_color_stop_rgba(1, 1, 1, 1, 0.3)
      context.set_source(lg)
      context.fill()

      # Stroking the circle
      self.reset(context)
      context.arc(50, 50, 300, 0, 2.0 * math.pi)
      context.set_source_rgb(0, 0, 0)
      context.stroke()

      # Painting an small rectangle
      self.reset(context)
      lg = cairo.LinearGradient(30, 0, 130, 0)
      lg.add_color_stop_rgba(0, 0, 1, 0, 1)
      lg.add_color_stop_rgba(1, 1, 1, 0, 0.5)
      context.rectangle(30, 330, 100, 60)
      context.set_source(lg)
      context.fill_preserve()
      context.set_source_rgb(0, 0, 0)
      context.stroke()


   def __draw_background(self, context):
      context.rectangle(0, 0, self.width, self.height)
      context.set_source_rgb(1, 1, 1)
      context.fill()

