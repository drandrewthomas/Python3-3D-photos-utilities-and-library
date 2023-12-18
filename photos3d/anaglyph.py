"""
anaglyph.py - Library module for loading and creating red-cyan anaglyph images.
"""

from PIL import Image

def create(lim, rim):
    # Both images must be same size
    lw, lh = lim.size
    agl = Image.new("RGB",(lw,lh),(255,255,255))
    lpix = lim.load()
    rpix = rim.load()
    aglpix = agl.load()
    for y in range(0, lh):
        for x in range(0, lw):
            left = lpix[x, y]
            right = rpix[x, y]
            aglpix[x, y] = (left[0], right[1], right[2])
    return agl

def load(fn, maxwid=None, rgb=True):
    pim = Image.open(fn)
    if maxwid != None:
        w, h = pim.size
        if w > maxwid:
            asp = w / h
            nh = int(maxwid / asp)
            pim = pim.resize((maxwid, nh), Image.LANCZOS)
    if rgb:
        if pim.mode == "RGBA":
            pim = pim.convert('RGB')
    return pim

def split(ang, gbmode="av"):
    aglw, aglh = ang.size
    lim = Image.new("RGB", (aglw, aglh), (255,255,255))
    rim = Image.new("RGB", (aglw, aglh), (255,255,255))
    apix = ang.load()
    lpix = lim.load()
    rpix = rim.load()
    for y in range(0, aglh):
        for x in range(0, aglw):
            col = apix[x, y]
            lc = int(col[0])
            lpix[x, y] = (lc, lc, lc)
            if gbmode == "green":
                rc = int(col[1])
            elif gbmode == "blue":
                rc = int(col[2])
            else:
                rc = int((col[1] + col[2]) /2)
            rpix[x, y] = (rc, rc, rc)
    return [lim, rim]


if __name__ == '__main__':
    print("Anaglyph module.")

