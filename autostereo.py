"""
autostereo.py - A simple example of using a depthmap image to create an autostereogram (sometimes called a magic eye image). The background is made up from a tile image which can be an image (preferably detailed) or a generated, mono or colour, random dot pattern.

Depth maps first need to be loaded and converted to a depth array that can be passed to the stereogram creation code. That allows the depth map to be adjusted - if you look at photos3d/depthmaps.py you'll see what they are (e.g. clearing ranges and remapping). And, of course, it allows you to write custom code to adjust them as a normal numpy array.
"""

import os

from photos3d import depthmaps as dmp

# Here's the important details for use in generating our steteogram.
fname = os.path.join(".", "testimages", "beeflower.jpg")
tilewid = 200
tilehgt = 200
tilex = 5
tiley = 5

# There's a number of ways to load the images, for example:
# 1. for just a depthmap image use
#dmap = dmp.load(fname)
#timg = dmp.make_random_pattern(50, 50, rgb=True, odds=1)
#
# 2. for RGB-D images use
timg, dmap = dmp.load(fname)
#
# 3. for RGB-D images with generated random dots
#_, dmap = dmp.load(fname)
#timg = dmp.make_random_pattern(50, 50, rgb=True, odds=1)

# We resize our tile image here, but we can omit this if we know it's already the correct size.'
timg = dmp.resize(timg, tilewid, tilehgt)

# Now we resize the depthmap image to make sure it's the same size as the stereogram will be. And we also convert it to a numpy array (depth value 0 ... 255).
dmap = dmp.resize(dmap, tilex * tilewid, tiley * tilehgt)
depths = dmp.depth_image_to_array(dmap, invert=True)

# And now we're ready to create our stereogram image.
sgimg = dmp.depth_to_autostereo(timg, tilex, tiley, depths, helpers=True)

# Uncomment to save it to an image file.
#sgimg.save("stereogram.png")

# Finally let's display the stereogram.'
from matplotlib import pyplot as plt
plt.imshow(sgimg)
plt.axis('off')
plt.show()
