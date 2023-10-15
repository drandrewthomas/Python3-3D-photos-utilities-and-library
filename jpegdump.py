"""
jpegdump.py - An example of using the jpegtool library module to print the structure of a JPG image file, as JPEG markers.
"""

import os

from photos3d import jpegtool as jpg

fname = "abbeystones.mpo" # MPO dual JPG container
#fname = "druidscircle.jpg" # JPEG image
#fname = "test.jps" # JPS containing single JPEG image
#fname = "classroom.vr.jpg" # Cardboard VR photo
#fname = "vr360.jpg" # 360 degree VR JPEG image

print("File: " + fname)
print()

fn = os.path.join(".", "testimages", fname)

flen, markers = jpg.find_markers(fn)

print("Bytes found: " + str(flen))
print()

jpg.pretty_print_markers(flen, markers, doblanks=True)
print()

exifs = jpg.get_exif_apps(fn, markers)
if len(exifs) == 0:
    print("No EXIF sections found.")
else:
    print("Exif section numbers: " + ", ".join(str(exif) for exif in exifs))
print()

xmps = jpg.get_xmp_apps(fn, markers)
if len(xmps) == 0:
    print("No XMP sections found.")
else:
    print("XMP section numbers: " + ", ".join(str(xmp) for xmp in xmps))
print()

exmps = jpg.get_extended_xmp_apps(fn, markers)
if not exmps:
    print("No extended XMP sections found.")
else:
    extxt = ""
    for ind, exmp in enumerate(exmps):
        extxt = extxt + str(exmp[0])
        if ind != (len(exmps) - 1):
            extxt = extxt + ", "
    print("Extended XMP section numbers: " + extxt)
print()

# Example of reading byte data from a jpeg section.
prsec = -1 # -1 for no listing
if prsec >= 0:
    nc = 100 # Num chars to print
    extrab = 10
    mtp = markers[prsec][3]
    etxt = ""
    if extrab > 0:
        etxt = " (+ <=" + str(extrab) + " bytes)"
    print()
    print("Section " + str(prsec) + " " + mtp + etxt + " listing:")
    dst = markers[prsec][1]
    dlen = markers[prsec][2]
    dsec = jpg.read_file_data(fn, dst, dlen+extrab)
    print()
    print(dsec[:nc])
    print()
    print(dsec[:nc].hex(' '))
