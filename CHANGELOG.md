# Changelog

## 15 October 2023

* Removed anabatch.py and mpobatch.py, together with the folders they used. Their functions can now be better obtained from the batch processing described below.

* Batch processing example batchprocess.py added (requires an imagestoprocess folder): note that files are overwritten for some processes such as swapping views and changing aspect ratios.

* Aspect ratio changing, preserving size, added to image library, with details of use in batch processing example.

* Image library now includes opening overlay images with transparency, and pasting overlays onto images (with mirrorx disparity option), plus an example in overlayimages.py.

* Added a jpegtool library with jpegdump (print jpg/mpo/jps file structure), cardsplit (cardboard photo splitting) and jpegsplit (extract images from MPO file) examples.

