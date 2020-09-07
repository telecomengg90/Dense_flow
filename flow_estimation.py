# -*- coding: utf-8 -*-
"""
Created on Mon Sep  7 16:38:15 2020

@author: Dell
"""
import cv2
import argparse
import sys
import numpy as np


keep_processing=True
np.set_printoptions(threshold=np.inf)
cap=cv2.VideoCapture("")   #add an abs path of image sequence

def draw_flow(img, flow, step=6):
    h, w = img.shape[:2]
    y, x = np.mgrid[step/2:h:step, step/2:w:step].reshape(2,-1).astype(int)
    fx, fy = flow[y,x].T


    #print(fx([635,611]))
    #print(fy)
    if (fy>4).all() and (fy<5).any():
     print(fy)

    #exproting the results to a text file as suggested by mr roman
    file1 = open("myfile.txt", "w")  # append mode
    file1.write(str(fx))
    file1.close()
    file2=open("myfile2.txt",'w')
    file2.write(str(fy))
    file2.close()
    for frames in range(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))):
     cv2.writeOpticalFlow("file"+str(frames)+".flo",flow)
    #np.savetxt('myfile.txt', x, delimiter=',')x


    lines = np.vstack([x, y, x+fx, y+fy]).T.reshape(-1, 2, 2)
    lines = np.int32(lines + 0.5)
    vis = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    cv2.polylines(vis, lines, 0, (0, 255, 0))


    for (x1, y1), (x2, y2) in lines:
        cv2.circle(vis, (x1, y1), 1, (0, 255, 0), -1)


    return vis
#cpturing of the images as suggested by mr roman

print(int(cap.get(cv2.CAP_PROP_FRAME_COUNT)))

#image1=cv2.imread("0149.png")
#image2=cv2.imread("0163.png")
ret,frame=cap.read()
prevgray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

for frames in range(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))):

    while (keep_processing):

        ret,frame2=cap.read()
        gray = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

        flow = cv2.calcOpticalFlowFarneback(prevgray, gray, None, 0.5, 5, 30, 5, 5, 1.1, 0)
        prevgray = gray

        windowName = "Dense Optic Flow" # window name

        cv2.imshow(windowName, draw_flow(gray, flow))




        key = cv2.waitKey(40) & 0xFF # wait 40ms (i.e. 1000ms / 25 fps = 40 ms)



        if (key == ord('x')):
         keep_processing = False
        elif (key == ord('f')):
                cv2.setWindowProperty(windowName, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

        # close all windows

cv2.destroyAllWindows()

