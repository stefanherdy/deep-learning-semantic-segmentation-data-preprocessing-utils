#!/usr/bin/env python3

"""
Script Name: find_scale.py
Author: Stefan Herdy
Date: 01.02.2023
Description: 
Read mask from ImageJ TIF-file and safe it as binary mask 

Usage: 
-  Set your data path and measure the scale of your images
"""

import os
from PIL import Image
import cv2
import numpy as np
from roifile import roiread


# Define the function to be executed on each image
def extract_mask(image_path):
    mask = np.zeros((1080, 1920))
    for i ,roi in enumerate(roiread(image_path)):
        #print(roi)
        #cv2.imshow('test', roi)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
        
        coor =  np.int32(np.asarray(roi.coordinates()))
        cv2.fillPoly(mask, pts =[coor], color=(255,255,255))

    return mask

# Define the path to the folder containing the images
folder_path = './data/'

# Iterate through all files in the folder
for filename in os.listdir(folder_path):
    # Check if the file is an image (JPEG or PNG)
    if filename.endswith('.tif'):
        # Construct the full path to the image
        image_path = os.path.join(folder_path, filename)
        # Execute the function on the image
        mask = extract_mask(image_path)
        cv2.imwrite('./mask/' + filename, mask)
        #cv2.imshow('test', mask)
        #cv2.waitKey(0) 
        #cv2.destroyAllWindows()


