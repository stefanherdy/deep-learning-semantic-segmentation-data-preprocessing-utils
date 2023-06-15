import cv2
import numpy as np

def get_scale(img_dir, name, plot = False):
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
                    print(name)
                    print('The length of 1000 Micrometers is ' + str(w) + 'Pixels.')
                    if plot == True:
                        cv2.imshow("Shapes", img)
                        cv2.waitKey(0)
                        cv2.destroyAllWindows()
    return w

if __name__ == '__main__':
    timesteps_int = [0,4,11,18,25,32,39,45,54,60,67,74,81,88,95]
    timesteps =['0', '04', '11', '18', '25', '32', '39', '45', '54', '60', '67', '74', '81', '88', '95']
    samplelist = ['06', '37', '39', '40', '44', '45', '46', '47']
    treatments = ['UN', 'SN', 'UL', 'SL', 'UH', 'SH']
    # Define the paths to the image and mask directories
    for _, sample in enumerate(samplelist):
        for _, treatment in enumerate(treatments):
            sizes = []
            for _, day in enumerate(timesteps):
                name = 'R' + sample + treatment + day + '.jpg'
                image_dir = './input_data/eval_data/R' + sample + '/' + '/R' + sample + treatment + '/' + name
                pix = get_scale(image_dir,name)

        