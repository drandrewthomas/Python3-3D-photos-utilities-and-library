"""
depth2sbs.py - An example of creating a side-by-side stereo 3D image using an RGBD file with the colour image on the left and the monochrome depth image on the right (you can do it other ways quite easily, including using separate rgb and depth files - see depthmaps.py - but this example uses a 2D photo conversion in that format created using the excellent DepthMaker Android app).
"""


import os

from photos3d import depthmaps as dm


fname = os.path.join(".", "testimages", "beeflower.jpg")

# First load the RGBD image (omit maxwid to keep original image sizes)
rgbim, depim = dm.load(fname, maxwid = 1000)

# Now we read the depth image pixel colour values into a numpy array
# and for images with white farthest away we need to invert the depths.
darr = dm.depth_image_to_array(depim, invert=True)

# We can also get possible values for the scale of disparity needed
dispnear, dispfar = dm.estimate_disparity(rgbim, strength='medium', converge='far')

# We create a vector for the depth (0...255) to disparity relationship
#dvec = dm.create_linear_disparity_vector(dispnear, dispfar)
dvec = dm.create_tangent_disparity_vector(dispnear*0.6, cvg = 0.5, fac=0.75) #cvg = 0.15, fac=1)

# And then we make the side-by-side stereo image
sbs = dm.depth_to_stereo(rgbim, darr, dvec, do3ddepth=False)

# The stereo picture is a Pillow image so we can save it
#sbs.save("sbs.png")

# Finally, let's have a look at our stereo 3D image:
from matplotlib import pyplot as plt
plt.imshow(sbs)
plt.axis('off')
plt.show()


