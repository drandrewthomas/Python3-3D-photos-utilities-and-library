# Python3 3D photos utilities and library

This repository contains a simple library, with examples, for loading and manipulating 3D photos and images in Python 3. The main code modules for the library can be found in the 'photos3d' folder.

<p align="center"><img src="markdownstuff/photos3d.png" alt="photos3d logo" /></p>

## Screenshots

Below are some screenshots to illustrate use of Photos3D in Python 3. They show loading and viewing side-by-side images, rotating stereo image pairs, creating an anaglyph from stereo image pairs and splitting a monochrome anaglyph into two stereo views.

<p align="center"><img src="markdownstuff/photos3dcollage.jpg" width="512" height="512" alt="Example output for rotating and cropping" /></p>

## Example Python 3 code

Example Python 3 code files are:

* anabatch.py - Converts all side-by-side images in the 'convertglyph' folder to anaglyphs.
* mpobatch.py - Converts all MPO files in the 'convertmpo' folder to side-by-side JPG files.
* makesbs.py - Example of making a side-by-side image from left and right image files.
* glyph2sbs.py - Example of how to split left and right views from a monochrome anaglyph.
* loadsbs.py - Example of loading MPO and side-by-side JPG files.
* rotatewithcrop.py - Example of loading and rotating side-by-side images with automatic cropping.
* sbs2glyph.py - Example of loading a side-by-side image and converting it to an anaglyph.

## Credits

The following sources of information and code are gratefully acknowledged:

The code in image.py for automagically cropping rotated images is [based on examples on Stack Overflow](https://stackoverflow.com/questions/16702966/rotate-image-and-crop-out-black-borders).

The formula in image.py to convert colours to luminance-based monochrome [is taken from Wikipedia](https://en.wikipedia.org/wiki/Grayscale).

This repository is copyright 2023 Andrew Thomas who also runs [parth3d.co.uk](https://parth3d.co.uk). Please enjoy them both :-)
