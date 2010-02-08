import gtk

# Class
# ==============================================================================
class Tool:
   CURSOR = gtk.gdk.Cursor(gtk.gdk.ARROW)

   def __init__(self, canvas):
      self.canvas = canvas

   def drag(self, x, y): pass

   def select(self):
      self.canvas.window.set_cursor(self.CURSOR)

   def begin(self, x, y): pass

   def end(self, x, y): pass

   def draw(self, context): pass


# Class 
# ==============================================================================
class BothScalingTool(Tool):
   CURSOR = gtk.gdk.Cursor(gtk.gdk.BOTTOM_RIGHT_CORNER)

   def drag(self, x, y):
      self.canvas.set_size(int(x), int(y))


# Class
# ==============================================================================
class HorizontalScalingTool(Tool):
   CURSOR = gtk.gdk.Cursor(gtk.gdk.RIGHT_SIDE)

   def drag(self, x, y):
      self.canvas.set_size(int(x), self.canvas.get_height())


# Class
# ==============================================================================
class VerticalScalingTool(Tool):
   CURSOR = gtk.gdk.Cursor(gtk.gdk.BOTTOM_SIDE)

   def drag(self, x, y):
      self.canvas.set_size(self.canvas.get_width(), int(y))

