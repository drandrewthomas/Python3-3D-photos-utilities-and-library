"""
batchprocess.py - An example utility script for batch processing a number of 3D photo files in one operation. Files must be in a folder called imagestoprocess. When the script is run a menu will allow you to choose operations to carry out on files in the folder.

REMEMBER THAT PHOTOS IN THE IMAGESTOPROCESS FOLDER WILL BE OVERWRITTEN BY SOME OPERATIONS SO BE VERY CAREFUL!

Currently using PNG, MPO, JPG, JPEG or JPS extensions only.
"""

import glob
import os

from photos3d import sbs as sbsim
from photos3d import anaglyph as glyph
from photos3d import image as img

def get_file_list(exts=["jpg", " jpeg", "jps", "png"]):
    exl = []
    for ext in exts:
        if ext.lower() not in exl:
            exl.append(ext.lower().strip())
        if ext.upper() not in exl:
            exl.append(ext.upper().strip())
    tflist = [] # Handle duplicates on Windows
    for ex in exl:
        dirpath = os.path.join(".", "imagestoprocess", "*." + ex)
        tflist = tflist + glob.glob(dirpath)
    flist = []
    for tf in tflist:
        if tf not in flist:
            flist.append(tf)
    return flist

def change_ext(path, ext):
    return os.path.splitext(path)[0] + '.' + ext

def do_menu():
    ch = ''
    while ch != 'x':
        print("a. Extract MPO files to side-by-side JPEGs.")
        print("b. Convert side-by-side JPEG files to anaglyphs.")
        print("c. Convert side-by-side JPEG files to mono anaglyphs.")
        print("d. Swap side-by-side left and right views.")
        print("e. Add mirrored bottoms to side-by-side images.")
        print("f. Pad to square (1:1) aspect ratio.")
        print("g. Pad to double square (2:1) aspect ratio.")
        print("x. Exit.")
        print()
        ch = input('Enter a choice: ').lower()
        print()
        if ch == 'a':
            batch_mpo_to_sbs()
        elif ch == 'b':
            batch_to_anaglyph(False)
        elif ch == 'c':
            batch_to_anaglyph(True)
        elif ch == 'd':
            batch_swap_sides()
        elif ch == 'e':
            batch_mirror_bottom()
        elif ch == 'f':
            batch_aspect_ratio(1)
        elif ch == 'g':
            batch_aspect_ratio(2)
        print()
        print()

def batch_mpo_to_sbs(quality=95):
    images = get_file_list(exts=["mpo"])
    print("Converting " + str(len(images)) + " MPO files to JPEG.")
    for fname in images:
        print("Converting file: " + fname)
        im = sbsim.load(fname)
        im.save(change_ext(fname, "jpg"), quality=quality)

def batch_to_anaglyph(mono, quality=95):
    images = get_file_list()
    if mono:
        print("Converting " + str(len(images)) + " files to mono anaglyphs:")
    else:
        print("Converting " + str(len(images)) + " files to anaglyphs:")
    print()
    for fname in images:
        print("Converting file: " + fname)
        lim, rim = sbsim.load(fname, dosplit=True)
        if mono:
            lim, rim = img.monochrome("luma", lim, rim)
        agl = glyph.create(lim, rim)
        agl.save(change_ext(fname, "anag.jpg"), quality=quality)

def batch_aspect_ratio(aspect, quality=95):
    images = get_file_list()
    print("Changing aspect ratio of " + str(len(images)) + " files to " + str(aspect) + " to 1:")
    print()
    for fname in images:
        fn, fext = os.path.splitext(fname)
        fext = fext.lower()
        if fext == ".jpg" or fext == ".jps" or fext == ".png":
            print("Converting file: " + fname)
            oimg = img.open(fname)
            aimg = img.change_aspect_ratio(aspect, oimg)
            aimg.save(fname, quality=quality)

def batch_swap_sides(quality=95):
    images = get_file_list()
    print("Swapping views for " + str(len(images)) + " files:")
    print()
    for fname in images:
        print("Swapping file: " + fname)
        lim, rim = sbsim.load(fname, dosplit=True)
        sbs = sbsim.create(rim, lim)
        sbs.save(fname, quality=quality)

def batch_mirror_bottom(quality=95):
    images = get_file_list()
    print("Adding mirrored bottom for " + str(len(images)) + " files:")
    print()
    for fname in images:
        print("Bottom mirroring file: " + fname)
        lim, rim = sbsim.load(fname, dosplit=True)
        sbs = sbsim.create(lim, rim)
        bsbs = sbsim.create(rim, lim)
        sbs = sbsim.create(sbs, bsbs, mode='ud')
        sbs.save(fname, quality=quality)


if __name__ == '__main__':
    fol = os.path.join(".", "imagestoprocess")
    if not os.path.exists(fol): 
        os.makedirs(fol)
        print("Created empty 'imagestoprocess' folder so exiting now!")
    else:
        do_menu()
        print("Finished.")
        print()

