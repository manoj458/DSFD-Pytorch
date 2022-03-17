import glob
import os
import cv2
import time
import face_detection
#from face_detection.retinaface.tensorrt_wrap import TensorRTRetinaFace
import numpy as np


def draw_faces(im, bboxes):
    for bbox in bboxes:
        x0, y0, x1, y1 = [int(_) for _ in bbox]
        cv2.rectangle(im, (x0, y0), (x1, y1), (0, 0, 255), 2)


if __name__ == "__main__":
    impaths = "images"
    impaths = glob.glob(os.path.join(impaths, "*.jpg"))
    #detector = face_detection.build_detector(
        #"DSFDDetector",
    #    "RetinaNetResNet50",
        #"RetinaNetMobileNetV1",
     #   max_resolution=1080
    #)
    batch_size = 3 
    detector = face_detection.build_detector(
               "DSFDDetector", 
               #"RetinaNetResNet50",
               ##confidence_threshold=.5, 
               #nms_iou_threshold=.3
        #       [batch_size, height, width, 3],
         #      images_dummy = np.zeros(batch_size, 512, 512, 3)
                max_resolution = 720
              )
    cap = cv2.VideoCapture('/data2/newyork_orig.mp4')    
    
    out_vid = cv2.VideoWriter('facedet_dfsd_trt__output1080.mp4', cv2.VideoWriter_fourcc('M','P','4','V'), 60.0, (1920,1080))

    skip_frames = 0

    write_frames = 999
    img_list = []
    while True:
        ret, im = cap.read()

        
        if ret == False:
            break
	
       # if write_frames % 5 !=0:
       #     img_list.append(im)
       #     continue
        
        
       
        if skip_frames != 0:
            skip_frames -= 1
            continue

        if write_frames == 0:
            break
       

        write_frames -= 1 
        #print(im.shape)
        #im = cv2.resize(im, (1920,1080))
        img_list = [im, im ]
        t = time.time()
        stacked_imgs = np.array(img_list)
        dets = detector.batched_detect(
            stacked_imgs
        )#[:, :4]
        print(f"Detection time: {time.time()- t:.3f}")
        draw_faces(stacked_imgs, dets)
       
        im = cv2.resize(stacked_imgs, (1280,720))
        out_vid.write(im)
        #cv2.imshow("streaming", im)
        #cv2.waitKey(1)
        img_list.clear()
