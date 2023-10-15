"""
loadsbs.py - An example of using the sbs module to load stereo pairs from image files in both JPG and MPO formats. Both formats are loaded using exactly the same syntax as the sbs module works out what to do.
"""

import os
from matplotlib import pyplot as plt
from photos3d import sbs as sbsim

sbsfname = os.path.join(".", "testimages", "bryncelliddu.jpg")
mpofname = os.path.join(".", "testimages", "abbeyflowers.mpo")

jpg = sbsim.load(sbsfname, 800)
mpo = sbsim.load(mpofname, 800)

fig=plt.figure()
fig.add_subplot(2,1,1)
plt.imshow(jpg)
plt.title("JPG file", fontsize=12)
fig.add_subplot(2,1,2)
plt.imshow(mpo)
plt.title("MPO file", fontsize=12)
fig.tight_layout()
plt.show()

