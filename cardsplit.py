"""
cardsplit.py - An example of how to use the jpegtool library module to extract the second image (of a stereo pair) from a Google Cardboard Camera panorama image (filename usually as *.vr.jpg).
"""

import os

from PIL import Image
from matplotlib import pyplot as plt

from photos3d import jpegtool as jpg
from photos3d import image as img
from photos3d import sbs as sbsim

print("Getting carboard image...")
fname = "classroom.vr.jpg"

fn = os.path.join(".", "testimages", fname)

print("File: " + fn)
print()

xmpimg = jpg.get_cardboard_image(fn)

print("Making side-by-side image...")

jpgimg = Image.open(fn)
w, h = jpgimg.size
l = (w / 2) - (h / 2)
left = img.crop(l, 0, l + h, h, jpgimg)
right = img.crop(l, 0, l + h, h, xmpimg)
sbs = sbsim.create(left, right)

print("Finished.")

if xmpimg == False:
    print("No embedded cardboard image found!")
else:
    fig=plt.figure()
    fig.add_subplot(3,1,1)
    plt.imshow(jpgimg)
    plt.title("Main JPEG image")
    fig.add_subplot(3,1,2)
    plt.imshow(xmpimg)
    plt.title("Extended XMP image")
    fig.add_subplot(3,1,3)
    plt.imshow(sbs)
    plt.title("Side-by-side image")
    plt.show()

