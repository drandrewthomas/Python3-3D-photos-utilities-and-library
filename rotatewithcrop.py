"""
rotatewithcrop.py - This is an example of how to load an image and rotate it using the
image module. It shows how that can be done with the image cropped to the largest area
rectangle based on the rotation angle. The example uses a JPG 3D photo but it works just
as well with an MPO file.
"""

import math, os
from matplotlib import pyplot as plt
from PIL import Image, ImageDraw
from photos3d import image as img
from photos3d import sbs as sbsimg

fname = os.path.join("testimages", "cosfordplane.jpg")
rang = -5 # Angle of rotation in degrees (in PIL negative is clockwise)

# First open left and right views from our test image and get the size
leftim, rightim = sbsimg.load(fname, 800, dosplit=True)
imw, imh = img.size(leftim)

# Next create two rotated versions for left and right, one cropped the other not
left_rotim, right_rotim = img.rotate(rang, leftim, rightim, docrop=False)
left_rotcropim, right_rotcropim = img.rotate(rang, leftim, rightim, docrop=True)

# Get the size of the image to crop to (as the rotation is the same we can
# use the same values for both left and right views)
cropw, croph = img.get_rotated_crop_size(imw, imh, rang)
rotimw, rotimh = img.size(left_rotim)
top = (rotimh / 2) - (croph / 2)
bot = (rotimh / 2) + (croph / 2)
lft = (rotimw / 2) - (cropw / 2)
rgt = (rotimw / 2) + (cropw / 2)

# Now draw that size box onto the uncropped images
left_draw = ImageDraw.Draw(left_rotim)
left_draw.line((lft, top, rgt, top), width=3, fill='red')
left_draw.line((lft, bot, rgt, bot), width=3, fill='red')
left_draw.line((lft, top, lft, bot), width=3, fill='red')
left_draw.line((rgt, top, rgt, bot), width=3, fill='red')
right_draw = ImageDraw.Draw(right_rotim)
right_draw.line((lft, top, rgt, top), width=3, fill='red')
right_draw.line((lft, bot, rgt, bot), width=3, fill='red')
right_draw.line((lft, top, lft, bot), width=3, fill='red')
right_draw.line((rgt, top, rgt, bot), width=3, fill='red')

# Finally we draw the images to the screen
fig=plt.figure()
fig.add_subplot(2,2,1)
plt.imshow(left_rotim)
plt.title("Left rotate", fontsize=12)
fig.add_subplot(2,2,2)
plt.imshow(right_rotim)
plt.title("Right rotate", fontsize=12)
fig.add_subplot(2,2,3)
plt.imshow(left_rotcropim)
plt.title("Left rotate and crop", fontsize=12)
fig.add_subplot(2,2,4)
plt.imshow(right_rotcropim)
plt.title("Right rotate and crop", fontsize=12)
fig.tight_layout()
plt.show()

