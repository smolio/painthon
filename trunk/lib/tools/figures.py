import cairo
from generic import Tool

class RectangleTool(Tool):
   initial_x = 0
   initial_y = 0
   final_x = 0
   final_y = 0

   def begin(self, x, y):
      self.initial_x = x
      self.initial_y = y
      self.final_x = x
      self.final_y = y

   def end(self, x, y):
      self.final_x = x
      self.final_y = y

   def draw(self, context):
      w = self.final_x - self.initial_x
      h = self.final_y - self.initial_y
      context.rectangle(self.initial_x, self.initial_y, w, h)
      context.set_source_rgb(0, 0, 1)
      context.fill_preserve()
      context.set_source_rgb(0, 0, 0)
      context.stroke()

   def drag(self, x, y):
      self.end(x, y)
