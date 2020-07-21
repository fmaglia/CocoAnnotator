# CocoAnnotator
COCO style format keypoint annotator for regression task on custom dataset.
This python script allows to annotate in COCO style format your custom dataset.
At the end of the process, it writes all the data in a JSON file (output.json).

# Requirements
* PIL
* OpenCV
* Tkinter

# Prerequisites
Remember to add the image folder path in python list_path.

# Usage
python3 coco_annotator.py

# Pipeline
* At the beginning you need to click to "Read image".
* Then, you can annotate your image clicking with left (visibile point) or wheel (not visibile point).
* When you click to "Annotate" the list of keypoints is added to a python dictionary. Moreover, the script moves to the next image to annotate.
* At the end, when you click to "Write" or when you finish the images to annotate, all the data are written to a JSON file in the COCO style format.
