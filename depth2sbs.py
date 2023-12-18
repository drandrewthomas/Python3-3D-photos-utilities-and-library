"""
depth2sbs.py - An example of creating a side-by-side stereo 3D image using an RGBD file with the colour image on the left and the monochrome depth image on the right (you can do it other ways quite easily, including using separate rgb and depth files - see depthmaps.py - but this example uses a Looking Glass 2D photo conversion in that format).
"""

import os

from photos3d import depthmaps as dm


fname = os.path.join(".", "testimages", "beeflower.jpg")

"""
You can just use the code below to get the side by side stereo image, but the code below that gives a fuller method that can be adapted to handle other, and more complicated, needs.

sbs = dm.quick_rgbd_to_stereo(fname, strength='medium', converge='far', maxwid=1000)
"""

# First load the RGBD image (omit maxwid to keep original image sizes)
rgbim, depim = dm.load(fname, maxwid = 1000)

# Now we read the depth image pixel colour values into a numpy array
darr = dm.depth_image_to_array(depim)

# We can also get possible values for the scale of disparity needed
dispmin, dispmax = dm.estimate_disparity(rgbim, strength='medium', converge='far')

# Next we calculate disparity values for the depth data
disps = dm.depth_array_to_disparity(darr, mindisp=dispmin, maxdisp=dispmax)

# And then we make the side-by-side stereo image
sbs = dm.depth_to_stereo(rgbim, disps)

# The stereo picture is a Pillow image so we can save it
#sbs.save("sbs.png")

# Finally, let's have a look at our stereo 3D image:
from matplotlib import pyplot as plt
plt.imshow(sbs)
plt.axis('off')
plt.show()


