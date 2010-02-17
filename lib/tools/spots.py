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

      target_color = pixels[x, y]
      pc = self.primary
      replacement_color = (int(pc.get_blue()*255), int(pc.get_green()*255),
                           int(pc.get_red()*255), int(pc.get_alpha()*255))

      self.__flood_fill(x, y, pixels, replacement_color, target_color)

      surface = ImageUtils.create_surface_from_image(image)
      self.canvas.set_image(surface)
      self.canvas.swap_buffers()

   def __flood_fill(self, x, y, pixels, replacement, target):
      edge = [(x, y)]
      pixels[x, y] = (replacement[0], replacement[1], replacement[2], 255)

      while edge:
         newedge = []
         for (x, y) in edge:
            for (s, t) in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
               if self.__within_image(s, t):
                  alpha = self.__compare(pixels[s, t], target)
                  if alpha != 0:
                     result = self.__mix_colors(pixels[s, t], replacement, alpha)
                     pixels[s, t] = result
                     newedge.append((s, t))
         edge = newedge


   def __within_image(self, x, y):
      if 0 <= x < self.canvas.get_width() and \
         0 <= y < self.canvas.get_height():
         return True
      return False


   def __compare(self, current, replacement):
      if current == replacement:
         return 255
      else:
         return 0


   def __mix_colors(self, current, replacement, alpha):
      calpha = (255-alpha)/255.0
      ralpha = alpha/255.0

      blue = current[0]*calpha + replacement[0]*ralpha
      green = current[1]*calpha + replacement[1]*ralpha
      red = current[2]*calpha + replacement[2]*ralpha

      return (blue, green, red, 255)


