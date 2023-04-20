"""
mpobathc.py - A utility program to read all MPO files in the convertmpo folder and
convert them to side-by-side images in JPEG files.
"""

import glob
import os
from photos3d import sbs as sbsim

dirpath = os.path.join(".", "convertmpo", "*.*")
images = glob.glob(dirpath)
print("Found " + str(len(images)) + " images.")
for fname in images:
    fn, fext = os.path.splitext(fname)
    if fext == ".mpo" or fext == ".MPO":
        print("Converting file: "+fname)
        im = sbsim.load(fname)
        im.save(fn+".jpg", quality=95)
    