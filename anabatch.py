"""
anabatch.py - A utility program to read all JPG stereo SBS files in the 'convertglyph' folder
and convert them to anaglyph images. You can change the mono variable to False if you want to
make colour anaglyphs.
"""

import glob
import os
from photos3d import sbs as sbsim
from photos3d import anaglyph as glyph
from photos3d import image as img

mono = True # Make monochrome anaglyph or not
dirpath = os.path.join(".", "convertglyph", "*.*")
images = glob.glob(dirpath)
print("Found " + str(len(images)) + " files.")
for fname in images:
    fn, fext = os.path.splitext(fname)
    if fext == ".jpg" or fext == ".JPG" \
    or fext == ".jpeg" or fext == ".JPEG" \
    or fext == ".png" or fext == ".PNG":
        print("Converting file: "+fname)
        lim, rim = sbsim.load(fname, dosplit=True)
        if mono:
            lim, rim = img.monochrome("luma", lim, rim)
        agl = glyph.create(lim, rim)
        agl.save(fn+"_anag.jpg", quality=95)
    