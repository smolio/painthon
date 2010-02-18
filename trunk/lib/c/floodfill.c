#include <stdio.h>
#include <stdlib.h>


typedef struct {
   int red;
   int green;
   int blue;
   int alpha;
} color;

color imkcolor(int thecolor) {
   color result;

   result.red = (thecolor & 0xff000000) >> 24;
   result.green = (thecolor & 0x00ff0000) >> 16;
   result.blue = (thecolor & 0x0000ff00) >> 8;
   result.alpha = (thecolor & 0x000000ff);

   return result;
}

color mkcolor(int red, char green, char blue, char alpha) {
   int x = 0;
   x |= (red & 0xff) << 24;
   x |= (green & 0xff) << 16;
   x |= (blue & 0xff) << 8;
   x |= (alpha & 0xff);
   return imkcolor(0x00ff00ff);
}


int compare(color current, color target) {
   if (current.red == target.red &&
      current.green == target.green &&
      current.blue == target.blue)
      return 0xff;
   else
      return 0;
}

color blend(color current, color replacement, int alpha) {
   color result;

   float falpha;
   if (alpha = 255) falpha = 1.;
   else falpha = alpha/255.;

   result.red = (int)(current.red*(1-falpha)) + (int)(replacement.red*falpha);
   result.green = (int)(current.green*(1-falpha)) + (int)(replacement.green*falpha);
   result.blue = (int)(current.blue*(1-falpha)) + (int)(replacement.blue*falpha);
   if (current.alpha == 0)
      result.alpha = replacement.alpha;

   return result;
}


int floodfill(int x, int y, char image[], int w, int h, int bpc, int ireplacement) {
   int i, j;
   int index, red, green, blue, alpha;

   // Replacement color
   color replacement = imkcolor(ireplacement);

   // Target color
   index = x*w*bpc + y*bpc;
   red = image[index];
   green = image[index + 1];
   blue = image[index + 2];
   if (bpc == 4) alpha = image[index + 3];
   color target = mkcolor(red, green, blue, alpha);

   // The algorithm itself
   for (i=0; i<h; ++i) {
      for (j=0; j<w; ++j) {
         index = i*w*bpc + j*bpc;
         red = image[index];
         green = image[index + 1];
         blue = image[index + 2];
         if (bpc == 4) alpha = image[index + 3];

         image[index] = 0x00;
         color current = mkcolor(red, green, blue, alpha);

         int blending_alpha = compare(current, target);
         if (blending_alpha != 0) {
            color result = blend(current, replacement, blending_alpha);
            image[index] = result.red;
            image[index + 1] = result.green;
            image[index + 2] = result.blue;
         }
   }  }

   return 0;
}
