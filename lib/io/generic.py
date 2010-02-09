import cairo
import gtk
import os
import gettext
from lib.graphics.canvas import Canvas

_ = gettext.gettext

class ImageFile:

   def __init__(self):
      png = PNGReaderWriter()

      self.TOOLS = { png.get_filter() : png }
      self.current_tool = None

   def open(self, path):
      file_dialog = gtk.FileChooserDialog(title=None,
         action=gtk.FILE_CHOOSER_ACTION_OPEN,
         buttons=(gtk.STOCK_CANCEL,
            gtk.RESPONSE_CANCEL,
            gtk.STOCK_OPEN, gtk.RESPONSE_OK)
         )

      for tool in self.TOOLS.values():
         file_dialog.add_filter(tool.get_filter())

      file_dialog.set_title(_("Open Image"))
      file_dialog.set_current_folder(path)

      response = file_dialog.run()
      if response == gtk.RESPONSE_OK:
         self.current_tool = self.TOOLS[file_dialog.get_filter()]
         result = self.current_tool.read(file_dialog.get_filename())
      else:
         result = None
      file_dialog.destroy()

      return result


   def save(self, image, path, filename=None):
      if filename == None:
         self.save_as(image, path)
      else:
         canonical_filename = path + os.sep + filename
         self.__detect_tool(filename)
         self.current_tool.write(image, canonical_filename)


   def save_as(self, image, path, filename=None):
      file_dialog = gtk.FileChooserDialog(title=None,
         action=gtk.FILE_CHOOSER_ACTION_SAVE,
         buttons=(gtk.STOCK_CANCEL,
            gtk.RESPONSE_CANCEL,
            gtk.STOCK_SAVE,
            gtk.RESPONSE_OK)
         )

      file_dialog.set_title(_("Save Image As"))
      file_dialog.set_current_folder(path)
      if filename != None:
         file_dialog.set_filename(filename)

      for tool in self.TOOLS.values():
         file_dialog.add_filter(tool.get_filter())

      response = file_dialog.run()
      if response == gtk.RESPONSE_OK:
         self.current_tool = self.TOOLS[file_dialog.get_filter()]
         self.current_tool.write(image, file_dialog.get_filename())
      file_dialog.destroy()


   def read(self, filename):
      self.__detect_tool(filename)
      return self.current_tool.read(filename)


   def __detect_tool(self, filename):
       # TODO: returning the proper tool according to filename's extension
      self.current_tool = self.TOOLS.values()[0]


class ReaderWriter:
   FILTER = None

   def get_filter(self):
      return self.FILTER

   def read(self, canonical_filename): pass
   def write(self, image, canonical_filename): pass


class PNGReaderWriter(ReaderWriter):
   def __init__(self):
      self.FILTER = gtk.FileFilter()
      self.FILTER.set_name("PNG - Portable Network Graphics")
      self.FILTER.add_mime_type("image/png")
      self.FILTER.add_pattern("*.png")


   def read(self, canonical_filename):
      return (canonical_filename,
         cairo.ImageSurface.create_from_png(canonical_filename),
         Canvas.TRANSPARENT_IMAGE)


   def write(self, image, canonical_filename):
      image.write_to_png(canonical_filename)


