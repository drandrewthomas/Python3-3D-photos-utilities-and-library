"""
sbs.py - Library for loading and creating side-by-side stereo image pairs.
"""

from PIL import Image
import os
import io

def create(lim, rim, mode='lr'):
    # Both images must be same size!
    w, h = lim.size
    if mode == 'ud':
        sbsim = Image.new("RGB", (w, h*2), (0, 0, 0))
        sbsim.paste(lim, (0, 0))
        sbsim.paste(rim, (0, h))
        return sbsim
    #Default to left-right ('lr')
    sbsim = Image.new("RGB", (w*2, h), (0, 0, 0))
    sbsim.paste(lim, (0, 0))
    sbsim.paste(rim, (w, 0))
    return sbsim

def load(fn, maxwid=None, rgb=True, dosplit=False, mode='lr'):
    fname, fext = os.path.splitext(fn)
    if fext == ".mpo" or fext == ".MPO":
        pim = Image.open(fn)
        pim.seek(0)
        lim = pim.copy()
        pim.seek(1)
        rim = pim.copy()
        im = create(lim, rim)
    else:
        im = Image.open(fn)
    if maxwid != None:
        w, h = im.size
        if w > maxwid:
            asp = w / h
            nh = int(maxwid / asp)
            im = im.resize((maxwid, nh), Image.LANCZOS)
    if rgb:
        if im.mode == "RGBA":
            im = im.convert('RGB')
    if dosplit:
        left, right = split(im, mode)
        im = [left, right]
    return im

def split(sbs, mode='lr'):
    sbsw, sbsh = sbs.size
    if mode == 'ud':
        nh = int(sbsh/2)
        top = sbs.crop((0, 0, sbsw, nh))
        bottom = sbs.crop((0, sbsh-nh, sbsw, sbsh))
        return [top, bottom]
    #Default to left-right ('lr')
    nw = int(sbsw/2)
    # Crop order: left, top, right, bottom
    left = sbs.crop((0, 0, nw, sbsh))
    # sbsw-nw ensures any odd width pixel is lost
    right = sbs.crop((sbsw-nw, 0, sbsw, sbsh))
    return [left, right]

if __name__ == '__main__':
    print("Tests in main")
    #im = load("../testimages/cosfordplane.jpg")
    
