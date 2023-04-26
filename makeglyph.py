"""
makeglyph.py - A simple example of loading a left and right image
from files and create an anaglyph picture to save.
"""

import os
from matplotlib import pyplot as plt
from photos3d import anaglyph as anag
from photos3d import image as img

if __name__ == '__main__':
    leftfname = os.path.join(".", "testimages", "lefttest.jpg")
    rightfname = os.path.join(".", "testimages", "righttest.jpg")
    left = img.open(leftfname)
    right = img.open(rightfname)
    glyph = anag.create(left, right)
    """
    This is a PIL image so to save the anaglyph picture use something like:
    outfname = os.path.join(".", "myimages", "myanaglyph.jpg")
    sbs.save(outfname)
    """
    plt.imshow(glyph)
    plt.show()
