"""
jpegsplit.py - An example of using the jpegtool library module to split individual images from a multiple JPEG container file (typically an MPO file). Only the first two images are displayed as is normal for stereo 3D image files. However, all images are extracted which could be useful for other container files.
"""
import os
from PIL import Image
from io import BytesIO
from matplotlib import pyplot as plt

from photos3d import jpegtool as jpg

fname = "abbeystones.mpo"
fn = os.path.join(".", "testimages", fname)

print("Splitting a JPEG file.")
print()
print("File: " + fn)
print()

flen, markers = jpg.find_markers(fn)

"""
Using split_images ensures we only get complete images starting with SOI and ending with EOI, which makes it easy to identify what data to read from the file.
"""

ims = jpg.split_images(markers)

print("Images found: " + str(len(ims)))
print()

if len(ims) < 2:
    print("Not enough images to split!")
    print()

if len(ims) > 1:
    fims = []
    for im in ims:
        st = im[0][1]
        en = im[-1][1] + im[-1][2]
        dl = en - st
        fim = jpg.read_file_data(fn, st, dl)
        img = Image.open(BytesIO(fim))
        fims.append(img)
    fig=plt.figure()
    fig.add_subplot(1,2,1)
    plt.imshow(fims[0])
    plt.title("First image")
    fig.add_subplot(1,2,2)
    plt.imshow(fims[1])
    plt.title("Second image")
    plt.show()

