"""
makesbs.py - A simple example of loading a left and right image from
files and create a side-by-side stereo pair.
"""

import os
from matplotlib import pyplot as plt
from photos3d import sbs as sbsim
from photos3d import image as img

if __name__ == '__main__':
    leftfname = os.path.join(".", "testimages", "lefttest.jpg")
    rightfname = os.path.join(".", "testimages", "righttest.jpg")
    left = img.open(leftfname)
    right = img.open(rightfname)
    sbs = sbsim.create(left, right)
    """
    This is a PIL image so to save the side-by-side picture use something like:
    outfname = os.path.join(".", "myimages", "myimage.jpg")
    sbs.save(outfname)
    """
    plt.imshow(sbs)
    plt.show()
