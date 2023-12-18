# Changelog

## 18 December 2023

* Added depthmaps.py library module for creating 3D stereo images using one RGB image and a corresponding monochrome depth image.

* Added depth2sbs.py as an example of using the depthmaps library module. It uses a new test image (beeflower.jpg) made using the Looking Glass AI 2D photo to 3D image convertor.

* Corrected some bugs in batchprocess.py that prevented operations on files with .jpeg extensions.

* The sbs.py library module now supports up-down and left-right 3D image formats.

* The batchprocess.py example now supports converting Google Cardboard panorama images (with 'vr.jpg' or 'vr.jpeg' file extensions only) to up-down jpeg files.

* Changed deprecated Pillow ANTIALIAS in resize methods to LANCZOS.

## 15 October 2023

* Removed anabatch.py and mpobatch.py, together with the folders they used. Their functions can now be better obtained from the batch processing described below.

* Batch processing example batchprocess.py added (requires an imagestoprocess folder): note that files are overwritten for some processes such as swapping views and changing aspect ratios.

* Aspect ratio changing, preserving size, added to image library, with details of use in batch processing example.

* Image library now includes opening overlay images with transparency, and pasting overlays onto images (with mirrorx disparity option), plus an example in overlayimages.py.

* Added a jpegtool library with jpegdump (print jpg/mpo/jps file structure), cardsplit (cardboard photo splitting) and jpegsplit (extract images from MPO file) examples.

