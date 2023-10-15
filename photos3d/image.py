"""
image.py - Library module for general image processing operations, mostly allowing for the same operation on two images in one call.
"""

import math
from PIL import Image, ImageEnhance, ImageFilter

def open(fname, rgb=True):
    im = Image.open(fname)
    if rgb:
        im = toRGB(im)
    return im

def open_overlay(fname, rgba=False):
    im = Image.open(fname)
    if rgba:
        im = toRGBA(im)
    return im

def size(img):
    imw, imh = img.size
    return [imw, imh]

def toRGB(img):
    nimg = img.convert('RGB')
    return nimg

def toRGBA(img):
    nimg = img.convert('RGBA')
    return nimg

def rotate(degrees, img, img2=None, docrop=True, doexpand=True, fill=(0, 0, 0)):
    imw, imh = img.size
    rotim = img.rotate(degrees, expand=doexpand, resample=Image.BICUBIC, fillcolor=fill)
    rw, rh = rotim.size
    if docrop == True and doexpand == True:
        cropw, croph = get_rotated_crop_size(imw, imh, degrees)
        top = (rh / 2) - (croph / 2)
        bot = (rh / 2) + (croph / 2)
        lft = (rw / 2) - (cropw / 2)
        rgt = (rw / 2) + (cropw / 2)
        rotim = crop(lft, top, rgt, bot, rotim)
    if img2 != None:
        rotim2 = rotate(degrees, img2, None, docrop, doexpand, fill)
        return [rotim, rotim2]
    return rotim

def crop(x0, y0, x1, y1, img, img2=None):
    cimg = img.crop((x0, y0, x1, y1))
    if img2 != None:
        cimg2 = img2.crop((x0, y0, x1, y1))
        return [cimg, cimg2]
    return cimg

def crop_roi(roi, img, img2=None):
    # Crop to region-of-interest as from undistortion (x, y, w, h)
    cimg = crop(roi[0], roi[1], roi[0]+roi[2], roi[1]+roi[3], img)
    if img2 != None:
        cimg2 = crop(roi[0], roi[1], roi[0]+roi[2], roi[1]+roi[3], img)
        return [cimg, cimg2]
    return cimg

def resize(nw, nh, img, img2=None):
    nim = img.resize((nw, nh), Image.ANTIALIAS)
    if img2 != None:
        nim2 = resize(nw, nh, img2)
        return [nim, nim2]
    return nim

def resize_width(nw, img, img2=None):
    ow, oh = img.size
    scl = nw / ow
    nh = int(oh * scl)
    nim = img.resize((nw, nh), Image.ANTIALIAS)
    if img2 != None:
        nim2 = resize_width(nw, img2)
        return [nim, nim2]
    return nim

def resize_height(nh, img, img2=None):
    ow, oh = img.size
    scl = nh / oh
    nw = int(ow * scl)
    nim = img.resize((nw, nh), Image.ANTIALIAS)
    if img2 != None:
        nim2 = resize_height(nh, img2)
        return [nim, nim2]
    return nim

def change_aspect_ratio(woverh, img, img2=None, back=(255, 255, 255)):
    w, h = img.size
    nw = h * woverh
    nh = w / woverh
    if nw > w:
        nh = nw / woverh
    else:
        nw = nh * woverh
    xoff = (nw - w) / 2
    yoff = (nh - h) / 2
    cimg = Image.new("RGB", (int(nw), int(nh)), back)
    cimg.paste(img, (int(xoff), int(yoff)))
    if img2 != None:
        cimg2 = change_aspect_ratio(woverh, img2, None, back)
        return [cimg, cimg2]
    return cimg

def overlay(x, y, ovl, img, ovl2=None, img2=None, mirrorx=False, alpha=True):
    # Overlay is pasted centred on image adjusted by x and y
    iw, ih = size(img)
    ow, oh = size(ovl)
    offx = (iw / 2) - (ow / 2) + x
    offy = (ih / 2) - (oh / 2) + y
    nim = Image.new("RGBA", (iw, ih), (0, 0, 0))
    nim.paste(img, (0, 0))
    if ovl.mode == "RGBA" and alpha:
        _, _, _, mask = ovl.split()
        nim.paste(ovl, (int(offx), int(offy)), mask)
    else:
        nim.paste(ovl, (int(offx), int(offy)))
    if img2 != None and ovl2 != None:
        if mirrorx:
            nim2 = overlay(-x, y, ovl2, img2)
        else:
            nim2 = overlay(x, y, ovl2, img2)
        return [nim, nim2]
    return nim

def brightness(bright, img, img2=None):
    enh = ImageEnhance.Brightness(img)
    enim = enh.enhance(bright)
    if img2 != None:
        enh = ImageEnhance.Brightness(img2)
        enim2 = enh.enhance(bright)
        return [enim, enim2]
    return enim

def contrast(cont, img, img2=None):
    enh = ImageEnhance.Contrast(img)
    enim = enh.enhance(cont)
    if img2 != None:
        enh = ImageEnhance.Contrast(img2)
        enim2 = enh.enhance(cont)
        return [enim, enim2]
    return enim

def get_anaglyph_brightness(img):
    imw, imh = img.size
    np = imw * imh
    r = g = b = 0
    pix = img.load()
    for ay in range(0, imh):
        for ax in range(0, imw):
            acol = pix[ax, ay]
            r = r +(acol[0] / np)
            g = r +(acol[1] / np)
            b = r +(acol[2] / np)
    return [r, (g + b) / 2]

def monochrome(mode, img, img2=None):
    imw, imh = img.size
    newimg = Image.new("RGB", (imw, imh), (255,255,255))
    opix = img.load()
    npix = newimg.load()
    for y in range(0, imh):
        for x in range(0, imw):
            col = opix[x, y]
            if mode == "average":
                luma = (col[0] + col[1] + col[2]) / 3
            elif mode == "luma":
                # From https://en.wikipedia.org/wiki/Grayscale for PAL/NTSC luminance
                luma = 0.299 * col[0] + 0.587 * col[1] + 0.114 * col[2]
            else:
                return False
            npix[x, y] = (int(luma), int(luma), int(luma))
    if img2 != None:
        newimg2 = monochrome(mode, img2)
        return [newimg, newimg2]
    return newimg

def findedges(img, img2=None):
    tim = img.convert("L")
    tim = tim.filter(ImageFilter.FIND_EDGES)
    edges = tim.convert('RGB')
    if img2 != None:
        edges2 = findedges(img2)
        return [edges, edges2]
    return edges

def swap_colour(cfrom, cto, img, img2=None, thresh=10):
    imw, imh = img.size
    newimg = Image.new("RGB", (imw, imh), (255,255,255))
    opix = img.load()
    npix = newimg.load()
    for y in range(0, imh):
        for x in range(0, imw):
            col = opix[x, y]
            if abs(col[0] - cfrom[0]) < thresh and abs(col[1] - cfrom[1]) < thresh and abs(col[2] - cfrom[2]) < thresh:
                npix[x, y] = cto
            else:
                npix[x, y] = col
    if img2 != None:
        newimg2 = swap_colour(cfrom, cto, img2, thresh=thresh)
        return [newimg, newimg2]
    return newimg

def get_rotated_crop_size(w, h, degrees, oddeven = None):
  #Based on: https://stackoverflow.com/questions/16702966/rotate-image-and-crop-out-black-borders
  if w <= 0 or h <= 0:
    return 0, 0
  angle = math.radians(degrees)
  width_is_longer = w >= h
  side_long, side_short = (w, h) if width_is_longer else (h, w)
  sin_a, cos_a = abs(math.sin(angle)), abs(math.cos(angle))
  if side_short <= 2. * sin_a * cos_a * side_long or abs(sin_a - cos_a) < 1e-10:
    x = 0.5 * side_short
    wr, hr = (x / sin_a, x / cos_a) if width_is_longer else (x / cos_a, x / sin_a)
  else:
    cos_2a = cos_a * cos_a - sin_a * sin_a
    wr, hr = (w * cos_a - h * sin_a) / cos_2a, (h * cos_a - w * sin_a) / cos_2a
    if oddeven == "odd":
        if int(wr) % 2 == 0: wr = wr -1
        if int(hr) % 2 == 0: hr = hr -1
    elif oddeven == "even":
        if int(wr) % 2 != 0: wr = wr -1
        if int(hr) % 2 != 0: hr = hr -1
  return int(wr), int(hr)


if __name__ == '__main__':
    print("Tests in main")
