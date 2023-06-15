#!/usr/bin/env python3

"""
Script Name: find_scale.py
Author: Stefan Herdy
Date: 01.02.2023
Description: 
Download your Labelbox annotations and save them as cathegorical imge file 

Usage: 
-  Download your export json-file from Labelbox
-  Set the path to your json-file
-  Set the path to your raw images
-  Update your label object names
"""

import json
import requests
import io
from PIL import Image
import urllib
import cv2
import shutil
import numpy as np



with open('path-to-your-json-file') as json_file:
    data = json.load(json_file)
    for i, d in enumerate(data):
        filename = data[i]['External ID']
        raw_img = cv2.imread('path-to-your-raw-images' + filename, -1)
        shape = np.shape(raw_img)
        mask_full = np.zeros(shape)
        classes = ['class1', 'class2', 'class3', 'class4']
        try:
            for idx, obj in enumerate(data[i]['Label']['objects']):
                URL = data[i]['Label']['objects'][idx]['instanceURI']
                for classname, j in enumerate(classes):
                    
                    if data[i]['Label']['objects'][idx]['title'] == classname:
                        cl = j
                    
                

                    with requests.get(URL, stream=True) as r:
                        with open("temp" + data[i]['External ID'] + ".jpg", "wb") as f:
                            r.raw.decode_content = True
                            shutil.copyfileobj(r.raw, f)
                    img = cv2.imread("temp" + data[i]['External ID'] + ".jpg", 0)

                    mask = np.where(img == 255)
                    mask_full[mask] = cl


            minv = np.min(mask_full)
            maxv = np.max(mask_full)
            unique = np.unique(mask_full)
            res_mask = cv2.resize(mask_full, (512, 512), interpolation = cv2.INTER_NEAREST)
            res_raw = cv2.resize(raw_img, (512, 512), interpolation = cv2.INTER_NEAREST)
            cv2.imwrite('masks/' + data[i]['External ID'] + '-mask.png', res_mask)
            cv2.imwrite('raw_images/' + data[i]['External ID'] + '-mask.png', res_raw)
        except:
            pass
