"""
pixelsmdepth.py - An example of splitting a Google Pixel 8 Pro portrait-mode photo, with the social media depth option enabled in the Pixel Camera app, and using the RGB and depthmap images to create a side-by-side stereo image. The code should work with other Pixel phones, and possibly even photos from other makes/models, with some modifications - as long as the photo is a container (similar to MPO files) for multiple images including a depth map.
"""

import os
import sys
from PIL import Image
from io import BytesIO
from matplotlib import pyplot as plt

from photos3d import jpegtool as jpg
from photos3d import image as img
from photos3d import depthmaps as dm

# First we need a depthmap enabled photo file
fname = "pixelsmdepthportrait.jpg"
fn = os.path.join(".", "testimages", fname)
print("Creating a stereo image from a Pixel phone portrait mode photo.")
print()
print("File: " + fn)
print()

# Next we find where the container images start and end
flen, markers = jpg.find_markers(fn)
ims = jpg.split_images(markers)
print("Images found: " + str(len(ims)))
print()

# In portrait mode on my Pixel 8 Pro the depthmap is at index 4.
# For other phones you may need to use trial and error to find
# the correct index value.
depthindex = 4

# Abort if there aren't enough embedded images
if len(ims) < (depthindex + 1):
    print()
    print("Not enough embedded images!")
    print("Perhaps SM Depth was not enabled?")
    print("Perhaps you need a different depth map index?")
    sys.exit()

# Now extract the RGB image (should be index zero)
st = ims[0][0][1]
en = ims[0][-1][1] + ims[0][-1][2]
dl = en - st
fdata = jpg.read_file_data(fn, st, dl)
rgb = Image.open(BytesIO(fdata))

# Then extract the depth map image in RGB format
st = ims[depthindex][0][1]
en = ims[depthindex][-1][1] + ims[depthindex][-1][2]
dl = en - st
fdata = jpg.read_file_data(fn, st, dl)
# Although monochrome, we need RGB depth map image!
depth = Image.open(BytesIO(fdata)).convert('RGB')
# Pixel depthmaps are black close and white far
depth = img.negative(depth)

# Reduce image size just to speed up this example
nw, nh = img.size(rgb)
rgb = img.resize(int(nw/2), int(nh/2), rgb)

# Make RGB and depth map images the same size
nw, nh = img.size(rgb)
depth = img.resize(nw, nh, depth)

# Now we can make a side-by-side stereo image
darr = dm.depth_image_to_array(depth)
dispmin, dispmax = dm.estimate_disparity(rgb, strength='low', converge='near')
disps = dm.depth_array_to_disparity(darr, mindisp=dispmin, maxdisp=dispmax)
sbs = dm.depth_to_stereo(rgb, disps, darr)

# Save our stereo image if we want (uncomment if wanted)
#sbs.save('sbs.jpg')

# Finally, we can plot the images
fig=plt.figure()
fig.add_subplot(2,2,1)
plt.imshow(rgb)
plt.title("RGB image")
fig.add_subplot(2,2,2)
plt.imshow(depth, cmap='gray')
plt.title("Depth image")
fig.add_subplot(2,1,2)
plt.imshow(sbs)
plt.title("SBS stereo output")
plt.tight_layout()
plt.show()


