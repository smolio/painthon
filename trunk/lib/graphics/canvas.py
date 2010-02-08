import cairo
import gtk
import math
from lib.tools.generic import *

class Canvas(gtk.DrawingArea):
   DEFAULT_CURSOR = gtk.gdk.Cursor(gtk.gdk.ARROW)
   active_tool = None
   drawing = False

   def __init__(self):
      # Initializing superclass
      super(Canvas, self).__init__()

      # Registering events
      #self.add_events(gtk.gdk.BUTTON_MOTION_MASK | gtk.gdk.BUTTON_PRESS | gtk.gdk.BUTTON_RELEASE)
      self.add_events(gtk.gdk.BUTTON_PRESS_MASK | gtk.gdk.BUTTON_RELEASE_MASK | gtk.gdk.BUTTON1_MOTION_MASK | gtk.gdk.DRAG_MOTION | gtk.gdk.POINTER_MOTION_MASK)
      self.connect("button-press-event", self.button_pressed)
      self.connect("button-release-event", self.button_released)
      self.connect("motion-notify-event", self.drag_event)
      self.connect("expose-event", self.expose)
      self.connect("motion-notify-event", self.motion_event)

      self.set_size(400, 300)
      self.image = cairo.ImageSurface.create_from_png("examples/flower.png")
      self.ALPHA_PATTERN = cairo.SurfacePattern(cairo.ImageSurface.create_from_png("pixmaps/alpha-pattern.png"))
      self.ALPHA_PATTERN.set_extend(cairo.EXTEND_REPEAT)

      # Basic tools
      self.DUMMY_TOOL = Tool(self)
      self.active_tool = self.DUMMY_TOOL

      # Final canvas
      self.CANVAS = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.width, self.height)


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


   def set_active_tool(self, tool):
      self.active_tool = tool


   def expose(self, widget, event):
      context = widget.window.cairo_create()

      self.draw(context)


   def button_pressed(self, widget, event):
      self.drawing = True
      self.active_tool.begin(event.x, event.y)


   def button_released(self, widget, event):
      self.active_tool.end(event.x, event.y)
      self.swap_buffers()
      self.print_tool()
      self.drawing = False


   def drag_event(self, widget, event):
      context = widget.window.cairo_create()
      self.active_tool.drag(event.x, event.y)
      self.swap_buffers()


   def motion_event(self, widget, event):
      self.active_tool.select()
      if event.x > self.width or event.y > self.height:
         self.window.set_cursor(self.DEFAULT_CURSOR)
         

   def print_tool(self):
      aux = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.width, self.height)
      context = cairo.Context(aux)
      self.draw(context)
      self.CANVAS = aux


   def draw(self, context):
      # Clipping area
      self.reset(context)

      # Drawing the background
      self.__draw_background(context)

      # Draw the result
      self.draw_image(context)
      if self.drawing:
         self.active_tool.draw(context)


   def draw_image(self, context):
      self.reset(context)

      source = context.get_source()
      context.set_source_surface(self.CANVAS)
      context.paint()
      context.set_source(source)


   def __draw_background(self, context):
      context.rectangle(0, 0, self.width, self.height)
      #context.set_source_rgb(1, 1, 1)
      #context.fill()
      context.set_source(self.ALPHA_PATTERN)
      context.paint()


   def swap_buffers(self):
      rect = gtk.gdk.Rectangle(0, 0, self.width, self.height)
      self.window.invalidate_rect(rect, True)
