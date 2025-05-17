# Changelog

## 17 May 2025

* The quick_rgbd_to_stereo function has been removed from the depthmaps.py library module as the full method shown in the depth2sbs.py example is quite simple to use.

* A new tangent-based depth to disparity method has been added to depthmaps.py and is now the default although the old linear method is still available if you prefer.

* The depthmaps.py library module has been updated to use a new depth to image method that calculates disparity from a depth (0...255) to disparity (pixels) relationship in a vector list. Other parts of the code have been updated to correspond to that change too.

* The depth_to_stereo method in depthmaps.py now has a do3ddepth parameter. It basically gives a quasi-spherical projection that is off by default, but can be fun to play with.

* The depth2sbs.py example has been updated to use the revised depthmaps.py library module.

## 21 March 2025

* The image 'beeflower.jpg' in the testimages folder has been replaced with a better version produced by the Android DepthMaker app.

* The function depth_image_to_array in depthmaps.py now has an option to invert depth values for depthmaps with white in the distance and black close up.

* The example depth2sbs.py has been updated to use the new 'beeflower.jpg' image with depth values inverted.

* Changed pixelsmdepth.py to give the option of either running the example or splitting JPG files in the imagestoprocess folder into rgb/depthmap pairs.

* Changed batchprocess.py to allow operations such as aspect ratio changing for PNG image files.

* Added mirrored bottom option to batchprocess.py which takes side-by-side images, makes a copy with left and right views swapped, and adds the swapped image below the original (i.e. a 4x4 image grid).

* Made a small change to batchprocess.py to stop a weird bug where a space was appended to file extensions in get_file_list (possibly this is a Pythonista thing, but the change should work everywhere else too).

## 26 July 2024

* Minor improvements to jpegtool.py module.

* When multiple extended XMP sections are found by get_extended_xmp_apps in jpegtool.py the first one is returned.

* The depthmaps.py module now includes use of depth buffering and prefilling with the original image in case some pixels don't get drawn to.

* The image.py module now has a negative image operation.

* The pixelsmdepth.py example is added to show how to convert a Pixel phone social media depth enabled portrait-mode photo (i.e. one with a depth map embedded within it) to a side-by-side stereo image.

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

