import os
import glob
import cv2
import time
import face_detection
#from face_detection.retinaface.tensorrt_wrap import TensorRTRetinaFace



def draw_faces(im, bboxes):
    for bbox in bboxes:
        x0, y0, x1, y1 = [int(_) for _ in bbox]
        cv2.rectangle(im, (x0, y0), (x1, y1), (0, 0, 255), 2)


if __name__ == "__main__":
    impaths = "images"
    impaths = glob.glob(os.path.join(impaths, "*.jpg"))
    detector = face_detection.build_detector(
        "DSFDDetector",
        #"RetinaNetResNet50",
        #"RetinaNetMobileNetV1",
        max_resolution=1080
    )


    cap = cv2.VideoCapture('video.mp4')    
    
    out_vid = cv2.VideoWriter('fbs3.mp4', cv2.VideoWriter_fourcc('M','P','4','V'), 30.0, (1280,720))

    skip_frames = 0

    write_frames = 5000

    while True:

        ret, im = cap.read()
        
        if ret == False:
            print("Failed")
            break 
	
           
           
        if skip_frames != 0:
            skip_frames -= 1
            continue

        if write_frames == 0:
           break
       
        write_frames -= 1 


        t = time.time()
        dets = detector.detect(
            im[:, :, ::-1]
        )[:, :4]
        print(f"Detection time: {time.time()- t:.3f}")
        #draw_faces(im, dets)

        for bbox in dets:
            x0, y0, x1, y1 = [int(_) for _ in bbox]
            sub_face = im[y0:y1, x0:x1]
            sub_face = cv2.GaussianBlur(sub_face,(23, 23), 30)
            if sub_face is None:
                continue
            #print(x0,y0,x1,y1)
            im[y0:y0+sub_face.shape[0], x0:x0+sub_face.shape[1]] = sub_face
        im = cv2.resize(im, (1280,720))
        out_vid.write(im)
        #cv2.imshow("streaming", im)
        #cv2.waitKey(1)
        
