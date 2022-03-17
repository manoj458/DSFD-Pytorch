import glob
import os
import cv2
import time
import face_detection


import numpy as np

import threading
import concurrent.futures

def draw_faces(im, bboxes):
    for bbox in bboxes:
        x0, y0, x1, y1 = [int(_) for _ in bbox]
        cv2.rectangle(im, (x0, y0), (x1, y1), (0, 0, 255), 2)

def blur_faces(im, bboxes,vwriter):
    print(bboxes)
    for bbox in bboxes:
        x0, y0, x1, y1 = [int(_) for _ in bbox]
        if x0<0:
            x0 = 0
        if y0<0:
            y0 = 0
        if x0>1278:
           x0 = 1278
        if y0>718:
           y0 = 718
        if x1<1:
            x1 = 1
        if y1<1:
            y1 = 1
        if x1>1279:
           x1 = 1279
        if y1>719:
           y1 = 719
        sub_face = im[y0:y1, x0:x1]
        sub_face = cv2.GaussianBlur(sub_face,(5, 5), 30)
        im[y0:y0+sub_face.shape[0], x0:x0+sub_face.shape[1]] = sub_face
    vwriter.write(im)


if __name__ == "__main__":
    impaths = "images"
    impaths = glob.glob(os.path.join(impaths, "*.jpg"))
    detector = face_detection.build_detector(
        "DSFDDetector",
        #"RetinaNetResNet50",
        max_resolution=1080
    )

    
    cap1 = cv2.VideoCapture('/data/newyork_orig.mp4')
    cap2 = cv2.VideoCapture('/data/newyork_orig.mp4')
    cap3 = cv2.VideoCapture('/data/newyork_orig.mp4')

    
    vwriter1 = cv2.VideoWriter('output1.avi', cv2.VideoWriter_fourcc('M','J','P','G'), 60.0, (1280,720))
    vwriter2 = cv2.VideoWriter('output2.avi', cv2.VideoWriter_fourcc('M','J','P','G'), 60.0, (1280,720))
    vwriter3 = cv2.VideoWriter('output3.avi', cv2.VideoWriter_fourcc('M','J','P','G'), 60.0, (1280,720))

    skip_frames = 3200

    fit1 = 0
    fit2 = 0
    fit3 = 0

    while True:

        t = time.time()

        ret1, im1 = cap1.read()
        ret2, im2 = cap2.read()
        ret3, im3 = cap3.read()


        if ret1 == False and ret2 == False and ret3 ==  False:
            break
        
        if ret1:
           im1 = cv2.resize(im1, (1280,720))
           with concurrent.futures.ThreadPoolExecutor() as executor:
               fit1 = executor.submit(detector.detect,im1)  
	   
        if ret2:
           im2 = cv2.resize(im2, (1280,720))
           with concurrent.futures.ThreadPoolExecutor() as executor:
               fit2 = executor.submit(detector.detect,im2)  

        if ret3:
           im3 = cv2.resize(im3, (1280,720))
           with concurrent.futures.ThreadPoolExecutor() as executor:
               fit3 = executor.submit(detector.detect,im3)  
        

        if ret1:
            x = threading.Thread(target = blur_faces, args = (im1, fit1.result()[:,:4], vwriter1), daemon=True)
            
        if ret2:
            y = threading.Thread(target = blur_faces, args = (im2, fit2.result()[:,:4], vwriter2), daemon=True)

        if ret3:
            z = threading.Thread(target = blur_faces, args = (im3, fit3.result()[:,:4], vwriter3), daemon=True)


        print(f"Total time elapsed: {time.time()- t:.3f}")
