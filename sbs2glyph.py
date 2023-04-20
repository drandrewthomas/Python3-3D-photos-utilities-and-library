"""
sbs2glyph.py - An example of how to load a side-by-side image from an MPO file
and convert it to an anaglyph image.
"""

import os
from photos3d import anaglyph as glyph
from photos3d import sbs as sbsim

fname = os.path.join(".", "testimages", "abbeyflowers.mpo")
left, right = sbsim.load(fname, maxwid=640*2, dosplit=True)
agl = glyph.create(left, right)

from matplotlib import pyplot as plt
plt.imshow(agl)
plt.show()
