"""
depthmaps.py - Library module for working with depth maps, such as for using them to convert RGB-D images to stereo pairs.

"""

import math
import numpy as np
from PIL import Image, ImageFilter


def load(fn1, fn2=None, maxwid=None):
    if fn2:
        img1 = __open_image_file__(fn1, maxwid=maxwid)
        img2 = __open_image_file__(fn2, maxwid=maxwid)
    else:
        if maxwid == None:
            img1 = __open_image_file__(fn1, None)
        else:
            img1 = __open_image_file__(fn1, 2 * maxwid)
        img1, img2 = __split_image__(img1)
    return [img1, img2]

def estimate_disparity(img, strength='medium', converge='far'):
    mindisp = maxdisp = 0
    dw, dh = img.size
    disp = dw * 0.03
    if strength == 'low':
        disp = dw * 0.04
    elif strength == 'medium':
        disp = dw * 0.07
    elif strength == 'high':
        disp = dw * 0.1
    elif isinstance(strength, (int, float)):
        disp = dw * strength
    if converge == 'far':
        mindisp = 0
        maxdisp = disp
    elif converge == 'middle':
        mindisp = - disp / 2
        maxdisp = disp / 2
    elif converge == 'near':
        mindisp = - disp
        maxdisp = 0
    elif isinstance(converge, (int, float)):
        if converge <= 1:
            mindisp = - (disp * converge)
            maxdisp = disp * (1 - converge)
    return [maxdisp, mindisp]

def depth_image_to_array(dimg, ch='red', invert=False):
    dw, dh = dimg.size
    depth = np.zeros((dh, dw), dtype="float32") # (rows, cols)
    dpix = dimg.load()
    for y in range(0, dh):
        for x in range(0, dw):
            col = dpix[x, y]
            if ch == 'red':
                depth[y, x] = col[0]
            elif ch == 'green':
                depth[y, x] = col[1]
            elif ch == 'blue':
                depth[y, x] = col[2]
            else:
                depth[y, x] = (col[0] + col[1] + col[2]) / 3
            if invert:
                depth[y, x] = 255 - depth[y, x]
    return depth

def create_linear_disparity_vector(neardisp, fardisp):
    dispvec = []
    for c in range(0, 256):
        dispvec.append(neardisp - ((c / 255) * (neardisp - fardisp)))
    return dispvec

def create_tangent_disparity_vector(neardisp, cvg = 0.15, fac=1):
    # neardisp is in pixels.
    # conv is 0.05 to 1 * total depth.
    # dfac is 0.1 to 10 * total depth:
    #     < 1 moves disparities toward far
    #     > 1 squashes them nearer zero
    disps = []
    conv = __constrain__(cvg, 0.05, 1)
    dfac = __constrain__(fac, 0.1, 10)
    cd = conv * 255 * dfac
    eyerot = math.atan((neardisp / 2) / cd)
    for c in range(0, 256):
        # Add half increment so we do not start at tan(zero)
        dist = (c * dfac) + (dfac / 2)
        #
        #dist = dist * 0.25
        #
        tang = math.atan((neardisp / 2) / dist)
        dang = 2 * ((tang + 1000) - (eyerot + 1000))
        disps.append(dang)
    df = neardisp / disps[0]
    for c in range(0, len(disps)):
        disps[c] = disps[c] * df
    return disps

def depth_to_stereo(rgbimg, depths, dispvect, prefill=True, blurfill=True, do3ddepth=True, dscl=None):
    """
    Note that for simplicity do3ddepth means the depth is calculated using pythagoras from the centre of the image (i.e. not from the two individual eye views).
    """
    imw, imh = rgbimg.size
    newimg = Image.new("RGB", (imw * 2, imh), (255, 255, 255))
    if prefill:
        if blurfill:
            newimg.paste(rgbimg.filter(ImageFilter.BLUR), (0, 0))
            newimg.paste(rgbimg.filter(ImageFilter.BLUR), (imw, 0))
        else:
            newimg.paste(rgbimg, (0, 0))
            newimg.paste(rgbimg, (imw, 0))
    opix = rgbimg.load()
    npix = newimg.load()
    dbuff = __blank_buffer__(imh, imw * 2) # rows, cols
    for y in range(0, imh):
        for x in range(0, imw):
            depth = depths[y, x]
            if do3ddepth:
                ##########
                # IS THIS THE RIGHT WAY TO COMPENSATE FOR DIFFERENT Z AXIS
                # SCALE COMPARED TO IMAGE WIDTH (X) AND HEIGHT (Y) ??????
                if dscl:
                    dscale = dscl
                else:
                    dscale = ((imw + imw) / 2) / 255
                depth = depth * dscale
                depth = math.sqrt(((x - (imw / 2)) * (x - (imw / 2))) + ((y - (imh / 2)) * (y - (imh / 2))) + (depth * depth))
                depth = depth / dscale
                ##########
                if depth > 255:
                    depth = 255
            disp = dispvect[int(depth)]
            ldx = x + (disp / 2)
            ldx = int(ldx + 0.5)
            if ldx < 0:
                ldx = 0
            if ldx >= imw:
                ldx = imw - 1
            rdx = x - (disp / 2)
            rdx = int(rdx + 0.5)
            if rdx < 0:
                rdx = 0
            if rdx >= imw:
                rdx = imw - 1
            if depth < dbuff[y, ldx]:
                dbuff[y, ldx] = depth
                npix[x, y] = opix[ldx, y]
            if depth < dbuff[y, rdx + imw]:
                dbuff[y, rdx + imw] = depth
                npix[x + imw, y] = opix[rdx, y]
    return newimg

# PRIVATE HELPER FUNCTIONS

def __map__(num, smin, smax, emin, emax):
    return (((num - smin) / (smax - smin)) * (emax - emin)) + emin

def __constrain__(nval, nmin, nmax):
    rv = nval
    if rv < nmin:
        rv = nmin
    if rv > nmax:
        rv = nmax
    return rv

def __open_image_file__(fname, maxwid=None):
    img = Image.open(fname)
    w, h = img.size
    if maxwid == None:
        if w % 2 != 0:
            img = img.crop((0, 0, w - 1, h))
    else:
        mwid = maxwid
        if mwid % 2 != 0:
            mwid = mwid - 1
        if w > mwid:
            asp = w / h
            nh = int(mwid / asp)
            img = img.resize((mwid, nh), Image.LANCZOS)
    if img.mode == "RGBA":
        img = img.convert('RGB')
    return img

def __split_image__(img):
    sbsw, sbsh = img.size
    nw = int(sbsw/2)
    left = img.crop((0, 0, nw, sbsh))
    right = img.crop((sbsw-nw, 0, sbsw, sbsh))
    return [left, right]

def __blank_buffer__(rows, cols, dep=99999999):
    buff = np.zeros((rows, cols), dtype="float32") # (rows, cols)
    for y in range(0, rows):
        for x in range(0, cols):
            buff[y, x] = dep
    return buff

def __array_info__(arr):
    avg = 0
    nav = 0
    amn = 999999
    amx = -999999
    dh, dw = arr.shape
    for y in range(0, dh):
        for x in range(0, dw):
            nav = nav + 1
            avg = avg + arr[y, x]
            if arr[y, x] < amn:
                amn = arr[y, x]
            if arr[y, x] > amx:
                amx = arr[y, x]
    avg = avg / nav
    return [amn, amx, avg]


if __name__ == '__main__':
    print("Depthmaps tests.")

