"""
jpegtool.py - Library for analysing JPEG files (e.g. jpg, jpeg, jps, mpo and the cardboard vr.jpg) and extracting data from them.
"""

jpeg_standards = [ "JPEG", "JPEG 1994", "JPEG 1997", "JPEG 2000", "JPEG-LS" ]

nolenmarkers = [ "SOI", "EOI", "TEM", "RST0", "RST1", "RST2", "RST3", "RST4", "RST5", "RST6", "RST7", "ERR" ]

jpeg_markers = [
  # From https://svn.xiph.org/experimental/giles/jpegdump.c [14 August 2023]
  [ 0x00, "NUL", "Zero byte stuffing", "JPEG" ],
  [ 0x01, "TEM", "reserved 01", "JPEG" ],
  [ 0xc0, "SOF0", "start of frame (baseline jpeg)", "JPEG 1994" ],
  [ 0xc1, "SOF1", "start of frame (extended sequential, huffman)", "JPEG 1994" ],
  [ 0xc2, "SOF2", "start of frame (progressive, huffman)", "JPEG 1994" ],
  [ 0xc3, "SOF3", "start of frame (lossless, huffman)", "JPEG 1994" ],
  [ 0xc5, "SOF5", "start of frame (differential sequential, huffman)", "JPEG 1994" ],
  [ 0xc6, "SOF6", "start of frame (differential progressive, huffman)", "JPEG 1994" ],
  [ 0xc7, "SOF7", "start of frame (differential lossless, huffman)", "JPEG 1994" ],
  [ 0xc8, "JPG", "reserved for JPEG extension", "JPEG 1994" ],
  [ 0xc9, "SOF9", "start of frame (extended sequential, arithmetic)", "JPEG 1994" ],
  [ 0xca, "SOF10", "start of frame (progressive, arithmetic)", "JPEG 1994" ],
  [ 0xcb, "SOF11", "start of frame (lossless, arithmetic)", "JPEG 1994" ],
  [ 0xcd, "SOF13", "start of frame (differential sequential, arithmetic)", "JPEG 1994" ],
  [ 0xce, "SOF14", "start of frame (differential progressive, arithmetic)", "JPEG 1994" ],
  [ 0xcf, "SOF15", "start of frame (differential lossless, arithmetic)", "JPEG 1994" ],
  [ 0xc4, "DHT", "define huffman tables", "JPEG 1994" ],
  [ 0xcc, "DAC", "define arithmetic coding conditioning", "JPEG 1994" ],
  [ 0xd0, "RST0", "restart marker 0", "JPEG 1994" ],
  [ 0xd1, "RST1", "restart marker 1", "JPEG 1994" ],
  [ 0xd2, "RST2", "restart marker 2", "JPEG 1994" ],
  [ 0xd3, "RST3", "restart marker 3", "JPEG 1994" ],
  [ 0xd4, "RST4", "restart marker 4", "JPEG 1994" ],
  [ 0xd5, "RST5", "restart marker 5", "JPEG 1994" ],
  [ 0xd6, "RST6", "restart marker 6", "JPEG 1994" ],
  [ 0xd7, "RST7", "restart marker 7", "JPEG 1994" ],
  [ 0xd8, "SOI", "start of image", "JPEG 1994" ],
  [ 0xd9, "EOI", "end of image", "JPEG 1994" ],
  [ 0xda, "SOS", "start of scan", "JPEG 1994" ],
  [ 0xdb, "DQT", "define quantization tables", "JPEG 1994" ],
  [ 0xdc, "DNL", "define number of lines", "JPEG 1994" ],
  [ 0xdd, "DRI", "define restart interval", "JPEG 1994" ],
  [ 0xde, "DHP", "define hierarchical progression", "JPEG 1994" ],
  [ 0xdf, "EXP", "expand reference components", "JPEG 1994" ],
  [ 0xe0, "APP0", "application data section  0", "JPEG 1997" ],
  [ 0xe1, "APP1", "application data section  1", "JPEG 1997" ],
  [ 0xe2, "APP2", "application data section  2", "JPEG 1997" ],
  [ 0xe3, "APP3", "application data section  3", "JPEG 1997" ],
  [ 0xe4, "APP4", "application data section  4", "JPEG 1997" ],
  [ 0xe5, "APP5", "application data section  5", "JPEG 1997" ],
  [ 0xe6, "APP6", "application data section  6", "JPEG 1997" ],
  [ 0xe7, "APP7", "application data section  7", "JPEG 1997" ],
  [ 0xe8, "APP8", "application data section  8", "JPEG 1997" ],
  [ 0xe9, "APP9", "application data section  9", "JPEG 1997" ],
  [ 0xea, "APP10", "application data section 10", "JPEG 1997" ],
  [ 0xeb, "APP11", "application data section 11", "JPEG 1997" ],
  [ 0xec, "APP12", "application data section 12", "JPEG 1997" ],
  [ 0xed, "APP13", "application data section 13", "JPEG 1997" ],
  [ 0xee, "APP14", "application data section 14", "JPEG 1997" ],
  [ 0xef, "APP15", "application data section 15", "JPEG 1997" ],
  [ 0xf0, "JPG0", "extension data 00", "JPEG 1997" ],
  [ 0xf1, "JPG1", "extension data 01", "JPEG 1997" ],
  [ 0xf2, "JPG2", "extension data 02", "JPEG 1997" ],
  [ 0xf3, "JPG3", "extension data 03", "JPEG 1997" ],
  [ 0xf4, "JPG4", "extension data 04", "JPEG 1997" ],
  [ 0xf5, "JPG5", "extension data 05", "JPEG 1997" ],
  [ 0xf6, "JPG6", "extension data 06", "JPEG 1997" ],
  [ 0xf7, "SOF48", "start of frame (JPEG-LS)", "JPEG-LS" ],
  [ 0xf8, "LSE", "extension parameters (JPEG-LS)", "JPEG-LS" ],
  [ 0xf9, "JPG9", "extension data 09", "JPEG 1997" ],
  [ 0xfa, "JPG10", "extension data 10", "JPEG 1997" ],
  [ 0xfb, "JPG11", "extension data 11", "JPEG 1997" ],
  [ 0xfc, "JPG12", "extension data 12", "JPEG 1997" ],
  [ 0xfd, "JPG13", "extension data 13", "JPEG 1997" ],
  [ 0xfe, "JCOM", "extension data (comment)", "JPEG 1997" ],
  [ 0x4f, "SOC", "start of codestream", "JPEG 2000" ],
  [ 0x90, "SOT", "start of tile", "JPEG 2000" ],
  [ 0xd9, "EOC", "end of codestream", "JPEG 2000" ],
  [ 0x51, "SIZ", "image and tile size", "JPEG 2000" ],
  [ 0x52, "COD", "coding style default", "JPEG 2000" ],
  [ 0x53, "COC", "coding style component", "JPEG 2000" ],
  [ 0x5e, "RGN", "region of interest", "JPEG 2000" ],
  [ 0x5c, "QCD", "quantization default", "JPEG 2000" ],
  [ 0x5d, "QCC", "quantization component", "JPEG 2000" ],
  [ 0x5f, "POC", "progression order change", "JPEG 2000" ],
  [ 0x55, "TLM", "tile-part lengths", "JPEG 2000" ],
  [ 0x57, "PLM", "packet length (main header)", "JPEG 2000" ],
  [ 0x58, "PLT", "packet length (tile-part header)", "JPEG 2000" ],
  [ 0x60, "PPM", "packed packet headers (main header)", "JPEG 2000" ],
  [ 0x61, "PPT", "packed packet headers (tile-part header)", "JPEG 2000" ],
  [ 0x91, "SOP", "start of packet", "JPEG 2000" ],
  [ 0x92, "EPH", "end of packet header", "JPEG 2000" ],
  [ 0x63, "CRG", "component registration", "JPEG 2000" ],
  [ 0x64, "COM", "comment", "JPEG 2000" ]
]

def get_marker_info(mbyte, standards=jpeg_standards):
    # Marker bytes are 0xff then 0xmbt
    for tag in jpeg_markers:
        if tag[3] in standards:
            if tag[0] == mbyte:
                return tag
    return [mbyte, "ERR", "Error unknown JPEG marker!"]

def read_file_data(fname, dst, dlen, asarray=False):
    with open(fname, "rb") as f:
        f.seek(dst)
        data = f.read(dlen)
        if asarray:
            data = bytearray(data)
        return data
    return False

def find_markers(fname, strictrst=True):
    mkrstart = False
    markers = []
    with open(fname, "rb") as f:
        inimage = False
        fpos = 0
        byte = f.read(1)
        while byte:
            if ord(byte) == 0xff:
                mkrstart = True
            elif mkrstart:
                # 0xff/0x00 is byte stuffing
                if ord(byte) == 0x00:
                    mkrstart = False
                # oxff/0xff is padding
                elif ord(byte) != 0xff:
                    mkrstart = False
                    mtp = get_marker_info(ord(byte))
                    if mtp[1] == "SOI":
                        if inimage:
                            print("Found consecutive SOI!")
                            return False
                        inimage = True
                    elif mtp[1] == "EOI":
                        if not inimage:
                            print("Found consecutive EOI!")
                            return False
                        inimage = False
                    if inimage or mtp[1] == "EOI":
                        if mtp[1] in nolenmarkers or mtp[1] == "SOS":
                            markers.append([ord(byte), fpos-1, 2, mtp[1]])
                        else:
                            b1 = f.read(1)
                            if b1 != False:
                                fpos = fpos + 1
                            b2 = f.read(1)
                            if b2 != False:
                                fpos = fpos + 1
                            if not b1 or not b2:
                                pass
                            else:
                                dlen = (ord(b1) * 256) + ord(b2) + 2
                                markers.append([ord(byte), fpos-3, dlen, mtp[1]])
                                for c in range(0, dlen - 4):
                                    b = f.read(1)
                                    if not b:
                                        break
                                    fpos = fpos + 1
            byte = f.read(1)
            fpos = fpos + 1
    if len(markers) == 0:
        print("No markers found in file!")
        return False
    insos = False
    sos = 0
    for c in range(0, len(markers)):
        if insos:
            if markers[c][3] == "SOS":
                print("Found SOS in SOS section data!")
                return False
            # RSTn markers are ignored in calculating SOS section length
            # as they only relate to SOS data and should not occur elsewhere.
            if not markers[c][3].startswith("RST"):
                markers[sos][2] = markers[c][1] - markers[sos][1]
                insos = False
        else:
            if markers[c][3].startswith("RST"):
                print("RST found outside SOS section!")
                if strictrst:
                    return False
            if markers[c][3] == "SOS":
                insos=True
                sos = c
    if insos:
        markers[sos][2] = fpos - markers[sos][1]
    return [fpos, markers]

def get_app_markers(markers, app=-1):
    apps = []
    tag = "APP"
    if app >= 0:
        tag = tag + str(app)
    for ind, marker in enumerate(markers):
        if marker[3].startswith(tag):
            apps.append(ind)
    return apps

def count_images(markers):
    ims = 0
    for marker in markers:
        if marker[3] == "EOI":
            ims = ims + 1
    return ims

def split_images(markers):
    # Any markers not within SOI/EOI ignored
    ims = []
    im = []
    stwait = True
    for marker in markers:
        if stwait:
            if marker[3] == "SOI":
                stwait = False
        if not stwait:
            im.append(marker)
            if marker[3] == "EOI":
                ims.append(im)
                im = []
                stwait = True
    return ims

def get_exif_apps(fname, markers=None, apps=None):
    tag = b"Exif"
    if markers == None:
        flen, markers = find_markers(fname)
    if markers == None or apps == None:
        apps = get_app_markers(markers, 1)
    exifs = []
    for app in apps:
        dst = markers[app][1] + 4
        dlen = markers[app][2] - 4
        if len(tag) <= dlen:
            std = read_file_data(fname, dst, len(tag))
            tpos = std.find(tag)
            if tpos == 0:
                exifs.append(app)
    return exifs

def get_xmp_apps(fname, markers=None, apps=None):
    tag = b"http://ns.adobe.com/xap/1.0/"
    if markers == None:
        flen, markers = find_markers(fname)
    if markers == None or apps == None:
        apps = get_app_markers(markers, 1)
    xmps = []
    for app in apps:
        dst = markers[app][1] + 4
        dlen = markers[app][2] - 4
        if len(tag) <= dlen:
            std = read_file_data(fname, dst, len(tag))
            tpos = std.find(tag)
            if tpos == 0:
                xmps.append(app)
    return xmps

def get_extended_xmp_apps(fname, markers=None, apps=None, dosort=True):
    tag = b"http://ns.adobe.com/xmp/extension/"
    if markers == None:
        flen, markers = find_markers(fname)
    if markers == None or apps == None:
        apps = get_app_markers(markers, 1)
    exmps = []
    for app in apps:
        dst = markers[app][1] + 4
        dlen = markers[app][2] - 4
        if dlen >= 75:
            std = read_file_data(fname, dst, 75)
            tpos = std.find(tag)
            if tpos == 0 and std[34] == 0x00:
                md5 = __bytes2string__(std[35 : 67])
                xlen = __bytes2uint__(std[67 : 71])
                xpos = __bytes2uint__(std[71 : 75])
                exmps.append([app, md5, xlen, xpos, dlen-75, dst+75])
    if len(exmps) == 0:
        return []
    etot = 0
    for exi in exmps:
        etot = etot + exi[4]
    if etot != exmps[0][2]:
        print("Wrong length extended XMP data found!")
        return []
    for ind, exm in enumerate(exmps):
        if ind == 0:
            md5 = exm[1]
        else:
            if exm[1] != md5:
                print("Don't yet handle multiple extended XMPs!")
                return []
    if dosort:
        exmps = sorted(exmps, key=lambda x: x[3])
    return exmps

def get_cardboard_image(fname, exmps=None):
    item = b'GImage:Data'
    b64 = get_extended_xmp_item(fname, item, exmps)
    from PIL import Image
    from io import BytesIO
    import base64
    cim = Image.open(BytesIO(base64.b64decode(b64 + b"==='")))
    return cim

def get_extended_xmp_item(fname, btext, exmps=None):
    # btext is a binary string
    if exmps == None:
        exmps = get_extended_xmp_apps(fname)
        if exmps == False:
            print("No extended xmp sections found!")
            return False
    stxt = b''.join([btext, b'="'])
    etxt = b'"'
    sa = sp = ea = ep = -1
    found = 0
    with open(fname, "rb") as f:
        for ind, xmp in enumerate(exmps):
            f.seek(xmp[5])
            data = f.read(xmp[4])
            if found == 0:
                ft = data.find(stxt)
                if ft != -1:
                    sa = ind
                    sp = ft + len(stxt)
                    found = 1
                    ft = data.find(etxt, ft + len(stxt))
                    if ft != -1:
                        ea = ind
                        ep = ft + len(etxt)
                        found = 2
            elif found == 1:
                ft = data.find(etxt)
                if ft != -1:
                    ea = ind
                    ep = ft + len(etxt)
                    found = 2
            elif found == 2:
                pass
        if sa == -1 or sp == -1 or ea == -1 or ep == -1:
            print("Couldn't find requested item in extended XMP!")
            return False
        txt = b''
        if sa == ea:
            f.seek(exmps[sa][5])
            txt = f.read(ep - sp - 1)
        else:
            for c in range(sa, ea+1):
                f.seek(exmps[c][5])
                adat = f.read(exmps[c][4])
                if c == sa:
                    adat = adat[sp:]
                elif c == ea:
                    adat = adat[:ep-1]
                txt = b''.join([txt, adat])
    # Binary syring returned!
    return txt

def pretty_print_markers(flen, markers, doblanks=True, aslist=False):
    lines = []
    lp = 0
    for c in range(0, len(markers)):
        mkstr = '{:<6d}  {:<5s}  {:<9d}  {:<8d}'.format(c, markers[c][3], markers[c][1], markers[c][2])
        trail = 0
        st = markers[c][1]
        if c == 0:
            if st > 0:
                bstr = '{:<6s}  {:<5s}  {:<9d}  {:<8d}'.format("", "BYTES", 0, st)
                if doblanks:
                    lines.append(bstr)
            lines.append(mkstr)
            lp = 0
        else:
            if not markers[c][3].startswith("RST"):
                le = markers[lp][1] + markers[lp][2] - 1
                if (st - 1) != le:
                    blank = st - le - 1
                    bstr = '{:<6s}  {:<5s}  {:<9d}  {:<8d}'.format("", "BYTES", le+1, blank)
                    if doblanks:
                        lines.append(bstr)
                lp = c
            lines.append(mkstr)
    le = markers[-1][1] + markers[-1][2]
    if le != flen:
        trail = flen - le
        bstr = '{:<6s}  {:<5s}  {:<9d}  {:<8d}'.format("", "BYTES", le, trail)
        if doblanks:
            lines.append(bstr)
    if aslist:
        return lines
    print('{:<6s}  {:<5s}  {:<9s}  {:<8s}'.format("Marker", "Tag", "Position", "Length"))
    print("------  ----   --------   ------")
    for line in lines:
        print(line)


# PRIVATE HELPER FUNCTIONS

def __bytes2uint__(bts):
    ui = bts[0] * 256 * 256 * 256
    ui = ui + bts[1] * 256 * 256
    ui = ui + bts[2] * 256
    ui = ui + bts[3]
    return ui

def __bytes2string__(bstr, chnull="[NULL]"):
    astr = ""
    for c in range(0, len(bstr)):
        if bstr[c] == 0:
            astr = astr + chnull
        else:
            astr = astr + chr(bstr[c])
    return astr

def __string2bytes__(str, encode="ascii"):
    return bytes(str, encoding=encode)
