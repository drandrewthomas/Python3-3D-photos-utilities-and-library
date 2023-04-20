from PIL import Image
import os
import io

def create(lim, rim):
    # Both images must be same size!
    w, h = lim.size
    sbsim = Image.new("RGB", (w*2, h), (0,0,0))
    sbsim.paste(lim, (0,0))
    sbsim.paste(rim, (w,0))
    return sbsim

def load(fn, maxwid=None, rgb=True, dosplit=False):
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
            im = im.resize((maxwid, nh), Image.ANTIALIAS)
    if rgb:
        if im.mode == "RGBA":
            im = im.convert('RGB')
    if dosplit:
        left, right = split(im)
        im = [left, right]
    return im

def split(sbs):
    sbsw, sbsh = sbs.size
    nw = int(sbsw/2)
    # Crop order: left, top, right, bottom
    left = sbs.crop((0, 0, nw, sbsh))
    # sbsw-nw ensures any odd width pixel is lost
    right = sbs.crop((sbsw-nw, 0, sbsw, sbsh))
    return [left, right]

if __name__ == '__main__':
    print("Tests in main")
    #im = load("../testimages/cosfordplane.jpg")
    