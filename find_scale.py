#!/usr/bin/env python3

"""
Script Name: find_scale.py
Author: Stefan Herdy
Date: 01.02.2023
Description: 
Automatically find and measure a scale in microscopy image

Usage: 
-  Set your data path and measure the scale of your images
"""

import cv2
import numpy as np

def get_scale(img_dir, plot = False):
    img = cv2.imread(img_dir)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(gray,253,255,cv2.THRESH_BINARY)
    #cv2.imshow('test', thresh)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    contours,hierarchy = cv2.findContours(thresh, 1, 2)
    print("Number of contours detected:", len(contours))
    #cv2.imshow('test', contours)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    for cnt in contours:
        x1,y1 = cnt[0][0]
        approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
        l = len(approx)
        if len(approx) <= 10:
            x, y, w, h = cv2.boundingRect(cnt)
            if w >=100:
                ratio = float(w)/h
                if ratio >= 5 and ratio <= 10:
                    img = cv2.drawContours(img, [cnt], -1, (0,255,255), 3)
                    cv2.putText(img, 'Scale', (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

                    print('------------------------')
                    print('The length of 1000 Micrometers is ' + str(w) + 'Pixels.')
                    if plot == True:
                        cv2.imshow("Shapes", img)
                        cv2.waitKey(0)
                        cv2.destroyAllWindows()
    return w

if __name__ == '__main__':
    image_dir = './data/Riccia_test.tif'
    pix = get_scale(image_dir)

        