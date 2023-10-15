"""
overlayimages.py - An example of loading a side-by-side image and pasting an overlay image/graphic, with an alpha channel, over the top. We could use a single overlay image, or split them from a stereo pair, but here we'll use two image files for left/right.
"""

import os
from matplotlib import pyplot as plt

from photos3d import sbs as sbsim
from photos3d import image as img

# First we load the stereo background image
fname = os.path.join(".", "testimages", "abbeyflowers.mpo")
lim, rim = sbsim.load(fname, dosplit=True)

# Next we load the left and right overlay images
lof = os.path.join(".", "testimages", "ghostoverlayleft.png")
rof = os.path.join(".", "testimages", "ghostoverlayright.png")
lov = img.open_overlay(lof)
rov = img.open_overlay(rof)

# We can ensure the overlay is no higher than the background image
iw, ih = img.size(lim)
lov, rov = img.resize_height(int(ih/2), lov, rov)

# Now we can overlay the images onto the background
x = -300 # Offsets from centre
y = 350
lim, rim = img.overlay(x, y, lov, lim, rov, rim)

# Then we recreate the stereo pair (optional, but makes plotting simpler)
sbs = sbsim.create(lim, rim)

# Finally we can display the stereo pair (or use sbs.save(outfilename) to save it)
plt.imshow(sbs)
plt.show()

