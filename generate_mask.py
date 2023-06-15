#!/usr/bin/python

import json
import requests
import io
from PIL import Image
import urllib
import cv2
import shutil
import numpy as np


img = cv2.imread('./input/testimg.jpg', -1)
#dim = (512, 512)
#resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
#cv2.imshow('test', resized)
#cv2.waitKey(0)
#cv2.destroyAllWindows()
#cv2.imwrite('input.jpg', resized)
minv = np.min(img)
maxv = np.max(img)
unique, idx = np.unique(img, return_index=True)

#mask_full = np.zeros((2128,2832))

with open('mask_files/segtest.json') as json_file:
    data = json.load(json_file)
    for i, d in enumerate(data):
        filename = data[i]['External ID']
        raw_img = cv2.imread('./raw_imgs/' + filename, -1)
        shape = np.shape(raw_img)
        mask_full = np.zeros(shape)
        ['Other', 'Toninia', 'Psora', 'Fulgensia', 'Placidium', 'Syntrichia', 'Collema', 'Cyano']
        try:
            for idx, obj in enumerate(data[i]['Label']['objects']):

                URL = data[i]['Label']['objects'][idx]['instanceURI']
                if data[i]['Label']['objects'][idx]['title'] == 'Not Classifiable':
                    cl = 0
                if data[i]['Label']['objects'][idx]['title'] == 'Toninia':
                    cl = 1
                if data[i]['Label']['objects'][idx]['title'] == 'Psora':
                    cl = 2
                if data[i]['Label']['objects'][idx]['title'] == 'Fulgensia':
                    cl = 3
                if data[i]['Label']['objects'][idx]['title'] == 'Placidium':
                    cl = 4
                if data[i]['Label']['objects'][idx]['title'] == 'Syntrichia':
                    cl = 5
                if data[i]['Label']['objects'][idx]['title'] == 'Collema':
                    cl = 6
                if data[i]['Label']['objects'][idx]['title'] == 'Cyanobacteria Dark':
                    cl = 7
                if data[i]['Label']['objects'][idx]['title'] == 'Cyanobacteria Pale':
                    cl = 7
                if data[i]['Label']['objects'][idx]['title'] == 'Vascular Plants':
                    cl = 7
                if data[i]['Label']['objects'][idx]['title'] == 'Soil':
                    cl = 7


                

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
            cv2.imshow('test', res_mask)
            cv2.imwrite('testmasks/' + data[i]['External ID'] + '-mask.png', res_mask)
            cv2.imwrite('input_imgs/' + data[i]['External ID'] + '-mask.png', res_raw)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            #classes = mask_full.unique()
        except:
            pass
    print('')