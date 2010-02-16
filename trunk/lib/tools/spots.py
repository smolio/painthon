from lib.graphics.imageutils import ImageUtils
from generic import Tool
from generic import DragAndDropTool

class ColorPickerTool(DragAndDropTool):
   pixels = None


   def begin(self, x, y):
      self.mode = self.DRAWING
      self.pixels = ImageUtils.create_image_from_surface(self.canvas.CANVAS).load()
      print self.pixels[x, y]


   def end(self, x, y):
      self.mode = self.READY
      print self.pixels[x, y]


   def move(self, x, y):
      if self.mode == self.DRAWING:
         print self.pixels[x, y]



class BucketFillTool(Tool):

   def begin(self, x, y):
      self.mode = self.READY
      image = ImageUtils.create_image_from_surface(self.canvas.CANVAS)

      pixels = image.load()

      # TODO: implement flood fil algorithm!
      for i in range(20):
         for j in range(20):
            pixels[x+i, y+j] = (255, 0, 255, 255)

      surface = ImageUtils.create_surface_from_image(image)
      self.canvas.set_image(surface)
      self.canvas.swap_buffers()

