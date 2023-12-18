import os
import numpy as np
from PIL import Image


def load(fn1, fn2=None, maxwid=None):
    if fn2:
        img1 = __open_image_file__(fn1, maxwid=maxwid)
        img2 = __open_image_file__(fn2, maxwid=maxwid)
    else:
        img1 = __open_image_file__(fn1, maxwid=(2*maxwid))
        img1, img2 = __split_image__(img1)
    return [img1, img2]

def quick_rgbd_to_stereo(fn1, fn2=None, strength='medium', converge='far', maxwid=None):
    rgbim, depim = load(fn1, fn2, maxwid=maxwid)
    darr = depth_image_to_array(depim)
    dispmin, dispmax = estimate_disparity(rgbim, strength=strength, converge=converge)
    disps = depth_array_to_disparity(darr, mindisp=dispmin, maxdisp=dispmax)
    sbs = depth_to_stereo(rgbim, disps)
    return sbs

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
    return [mindisp, maxdisp]

def depth_image_to_array(dimg, ch='red'):
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
    return depth

def depth_array_to_disparity(depth, mindisp=-10, maxdisp=10, params=None):
    if params == None:
        amn, amx, avg = __array_info__(depth)
    else:
        amn = params[0]
        amx = params[1]
    dh, dw = depth.shape
    disp = np.zeros((dh, dw), dtype="float32") # (rows, cols)
    for y in range(0, dh):
        for x in range(0, dw):
            dep = depth[y, x]
            if dep < amn:
                dep = amn
            if dep > amx:
                dep = amx
            disp[y, x] = __map__(dep, amn, amx, mindisp, maxdisp)
    return disp

def depth_to_stereo(rgbimg, disps):
    imw, imh = rgbimg.size
    newimg = Image.new("RGB", (imw * 2, imh), (255, 255, 255))
    opix = rgbimg.load()
    npix = newimg.load()
    for y in range(0, imh):
        for x in range(0, imw):
            disp = disps[y, x]
            dx = x - (disp / 2)
            if dx < 0:
                dx = 0
            if dx >= imw:
                dx = imw - 1
            npix[x, y] = opix[dx, y]
            dx = x + (disp / 2)
            if dx < 0:
                dx = 0
            if dx >= imw:
                dx = imw - 1
            npix[x + imw, y] = opix[dx, y]
    return newimg


# PRIVATE HELPER FUNCTIONS

def __map__(num,smin,smax,emin,emax):
    return (((num-smin)/(smax-smin))*(emax-emin))+emin

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
            img = img.resize((mwid, nh), Image.ANTIALIAS)
    if img.mode == "RGBA":
        img = img.convert('RGB')
    return img

def __split_image__(img):
    sbsw, sbsh = img.size
    nw = int(sbsw/2)
    left = img.crop((0, 0, nw, sbsh))
    right = img.crop((sbsw-nw, 0, sbsw, sbsh))
    return [left, right]

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

