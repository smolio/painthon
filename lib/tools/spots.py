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

      self.__flood_fill((x,y), pixels, replacement_color, target_color)

      surface = ImageUtils.create_surface_from_image(image)
      self.canvas.set_image(surface)
      self.canvas.swap_buffers()

   def __flood_fill(self, point, pixels, replacement, target):
      stack = list()
      stack.append(point)

      while len(stack) > 0:
         cur_pix = stack.pop()
         cur_col = pixels[cur_pix[0], cur_pix[1]]

         if cur_col[0:3] == replacement[0:3]:
            continue

         alpha = self.__compare(cur_col[0:3], target[0:3])
         if alpha != 0:
            res = self.__mix_colors(cur_col[0:3], replacement[0:3], alpha)
            pixels[cur_pix[0], cur_pix[1]] = res

            # North:
            if cur_pix[1] >= 1:
               stack.append((cur_pix[0], cur_pix[1]-1))

            # South:
            if cur_pix[1] < self.canvas.get_height()-1:
               stack.append((cur_pix[0], cur_pix[1]+1))

            # West:
            if cur_pix[0] >= 1:
               stack.append((cur_pix[0]-1, cur_pix[1]))

            # East:
            if cur_pix[0] < self.canvas.get_width()-1:
               stack.append((cur_pix[0]+1, cur_pix[1]))

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
