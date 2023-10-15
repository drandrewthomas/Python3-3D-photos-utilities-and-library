"""
glyph2sbs.py - A simple example of splitting left and right views from a monochrome anaglyph image. Because the left and right eye views were created from different colours you may need to adjust their brightness and contrast levels individually to get a usable stereo pair.
"""

import os
from matplotlib import pyplot as plt
from photos3d import anaglyph as glyph
from photos3d import sbs as sbsim
from photos3d import image as img

fname = os.path.join(".", "testimages", "druidsglyph.png")
agl = glyph.load(fname, 640)
lb, rb = img.get_anaglyph_brightness(agl)
print("Av left: "+str(lb))
print("Av right: "+str(rb))
left, right = glyph.split(agl)
right = img.contrast(1.2, right)
right = img.brightness(1.2, right)
sbs = sbsim.create(left, right)
plt.imshow(sbs)
plt.show()

