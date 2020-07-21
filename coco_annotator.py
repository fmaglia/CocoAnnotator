import time
import tkinter.messagebox
from tkinter import *
import cv2 as cv
import numpy as np
from PIL import Image as PIL_Image
from PIL import ImageTk as PIL_ImageTk
from PIL import ImageDraw
from IPython import embed
import os
import shutil
import datetime
import glob
import json

def callback(event):
    print ("left clicked at: ", event.x, event.y)
    global pts
    pts.append([event.x, event.y, 2])
    global panel
    global list_images
    global image_idx

    image = cv.imread(list_images[image_idx])
    for elem in pts:
        cv.circle(image,(int(elem[0]),int(elem[1])), 3, (0,255,0), -1)
    image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    
    pil_img = PIL_Image.fromarray(image)
    photo1 = PIL_ImageTk.PhotoImage(pil_img)
    panel.configure(image=photo1)
    panel.photo = photo1

def callback2(event):
    print ("right clicked at: ", event.x, event.y)
    global pts
    pts.append([event.x, event.y, 1])
    global panel
    global list_images
    global image_idx

    image = cv.imread(list_images[image_idx])
    for elem in pts:
        cv.circle(image,(int(elem[0]),int(elem[1])), 3, (255,0,0), -1)
    image = cv.cvtColor(image, cv.COLOR_BGR2RGB)

    pil_img = PIL_Image.fromarray(image)
    photo1 = PIL_ImageTk.PhotoImage(pil_img)
    panel.configure(image=photo1)
    panel.photo = photo1

def append_json(filename, json_dict):
    with open(filename, 'a') as json_file:
        json.dump(json_dict, json_file, indent=15)

def write_json(filename, json_dict):
    with open(filename, 'w') as json_file:
        json.dump(json_dict, json_file, indent=15)
    print("Write on JSON completed")

def read_image(list_images, label):
    global image_idx
    #image = cv.imread(list_images[image_idx])
    
    pil_img = PIL_Image.open(list_images[image_idx])
    photo1 = PIL_ImageTk.PhotoImage(pil_img)
    label.configure(image=photo1)
    label.photo = photo1
    print("current idx",image_idx)

    json_dict = {"filename": list_images[image_idx],
    "height": pil_img.size[1],
    "width": pil_img.size[0],
    "id": image_idx
    }
    append_json("coco_images.json", json_dict)


    global pts 
    pts = []

def clean_list():
    global pts
    pts = []
    pass

def annotate(label):
    print("Annotation.")
    # print(pts)
    global pts
    global image_idx
    global list_images
    # img = cv.imread(list_images[image_idx])
    print (pts)
    kpts = []
    for i in range(len(pts)):
        kpts += pts[i]
    global json_dict
    print("Append to JSON dict")

    # embed()

    json_dict["annotations"].append(  {
                "num_keypoints": len(pts),
                # "area": img.shape[0]*img.shape[1],
                "keypoints": kpts,
                "image_id": image_idx,
                "id": image_idx
            })

    pts = []
    image_idx += 1
    if (image_idx == len(list_images)):
        write_json("robish.json", json_dict)
    
    global panel
    read_image(list_images, panel)
    pass

if __name__ == '__main__':
    print('Example started')

    json_dict = {
        "info": {
            "description": "My Dataset",
            "url": "http://magliani.altervista.org",
            "version": "1.0",
            "year": 2020,
            "contributor": "Federico Magliani",
            "date_created": "2020/07/21"
        },
        "licenses": [
            {
                "url": "http://creativecommons.org/licenses/by-nc-sa/2.0/",
                "id": 0,
                "name": "Attribution-NonCommercial-ShareAlike License"
            }
        ],
        "images": [
            {
                #"license": 4,
                "file_name": "000000397133.jpg",
                "coco_url": "http://images.cocodataset.org/val2017/000000397133.jpg",
                "height": 427,
                "width": 640,
                #"date_captured": "2013-11-14 17:02:52",
                #"flickr_url": "http://farm7.staticflickr.com/6116/6255196340_da26cf2c9e_z.jpg",
                "id": 397133
            }
    
        ],
        "annotations": [
            {
                #"segmentation": [[204.01,306.23,...206.53,307.95]],
                "num_keypoints": 15,
                # "area": 5463.6864,
                #"iscrowd": 0,
                "keypoints": [229,256,2,223,369,2],
                "image_id": 289343,
                #"bbox": [204.01,235.08,60.84,177.36],
                #"category_id": 1,
                "id": 201376
            }
        ]
    }
    

    list_images = []
    pts = []
    list_path = ["/home/federico/imgTriton",
    "/home/federico/imgRealsense"]

    for j in range(len(list_path)):
        str_condition = list_path[j]+"/*.jpg"
        for name in glob.glob(str_condition):
            list_images.append(name)
    
    print("Images",len(list_images))

    image_idx = 0
    for i in range(len(list_images)):
        image = cv.imread(list_images[i])
        json_dict['licenses'].append(            {
                "url": "http://creativecommons.org/licenses/by-nc-sa/2.0/",
                "id": i,
                "name": "Attribution-NonCommercial-ShareAlike License"
            })

        json_dict['images'].append(
                {
            "file_name": list_images[i],
            #"coco_url": "http://images.cocodataset.org/val2017/000000397133.jpg",
            "height": image.shape[0],
            "width": image.shape[1],
            #"date_captured": "2013-11-14 17:02:52",
            #"flickr_url": "http://farm7.staticflickr.com/6116/6255196340_da26cf2c9e_z.jpg",
            "id": i
        })
    # remove example elements added to python dictionary
    del json_dict["licenses"][0]
    del json_dict["images"][0]
    del json_dict["annotations"][0]
    
    root = Tk()
    root.title('COCO style format dataset Annotator')
    frame = Frame(root)
    frame.pack()
    
    pil_img = PIL_Image.new('RGB', (1440, 1080))

    img = PIL_ImageTk.PhotoImage(pil_img)
    
    panel = Label(frame, image = img)

    button = Button(frame, 
                   text="Read image", 
                   fg="red",
                   command = lambda: read_image(list_images, panel))
    button.pack(side=LEFT)

    button_clean = Button(frame, 
                   text="Clean list", 
                   fg="red",
                   command = lambda: clean_list())
    button_clean.pack(side=LEFT)

    button = Button(frame, 
                   text="Annotate", 
                   fg="red",
                   command = lambda: annotate(panel))
    button.pack(side=LEFT)

    button_write = Button(frame, 
                   text="Write", 
                   fg="red",
                   command = lambda: write_json('robish.json',json_dict))
    button_write.pack(side=LEFT)

    panel.bind('<Button-1>', callback)
    panel.bind('<Button-2>', callback2)
    
    panel.pack(side = LEFT)

    root.mainloop()

    print('Annotation completed successfully')
