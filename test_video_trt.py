import os
os.environ["CUDA_VISIBLE_DEVICES"]="1"
import glob
import cv2
import time
import face_detection
from face_detection.retinaface.tensorrt_wrap import TensorRTRetinaFace



def draw_faces(im, bboxes):
    for bbox in bboxes:
        x0, y0, x1, y1 = [int(_) for _ in bbox]
        cv2.rectangle(im, (x0, y0), (x1, y1), (0, 0, 255), 2)


if __name__ == "__main__":
    impaths = "images"
    impaths = glob.glob(os.path.join(impaths, "*.jpg"))
    detector = face_detection.build_detector(
        #"DSFDDetector",
        "RetinaNetResNet50",
        #"RetinaNetMobileNetV1",
        max_resolution=1080
    )


    cap = cv2.VideoCapture('face_blurring_sample_video.avi')    
    
    out_vid = cv2.VideoWriter('fbs_out_res50trt.mp4', cv2.VideoWriter_fourcc('M','P','4','V'), 30.0, (1280,720))

    inference_imshape =(480, 640) # Input to the CNN
    input_imshape = (720, 1280) # Input for original video source
    detector = TensorRTRetinaFace(input_imshape,inference_imshape)
    skip_frames = 0

    write_frames = 4000

    while True:

        ret, im = cap.read()

        im = cv2.resize(im,(1280,720))
        if ret == False:
            break
        
	
           
           
        if skip_frames != 0:
            skip_frames -= 1
            continue

        if write_frames == 0:
           break
       
        write_frames -= 1 

        start = time.time()
        image = im
        #inference_imshape =(480, 640) # Input to the CNN
        #input_imshape = (1080,1920) # Input for original video source
        #detector = TensorRTRetinaFace(input_imshape,inference_imshape)
        boxes, landmarks, scores = detector.infer(image)
        end = time.time()
        start1 = time.time()
        print("time elapsed TRTInfer: ",(end-start))
        for i in range(boxes.shape[0]):
            #print(boxes[i])
            #print(scores)
            x0, y0, x1, y1 = boxes[i].astype(int)
            image = cv2.rectangle(image, (x0, y0), (x1, y1),(0, 0, 255), 2 )
            #for kp in landms[i]:
            #    image = cv2.circle(image, tuple(kp), 5, (255, 0, 0))
        #image = cv2.resize(im,(1280,720))
        out_vid.write(image)
        end1 = time.time()
        print("time elapsed draw and record: ",(end1-start1))
        continue

        t = time.time()
        dets = detector.detect(
            im[:, :, ::-1]
        )[:, :4]
        print(f"Detection time: {time.time()- t:.3f}")
        draw_faces(im, dets)
       
        im = cv2.resize(im, (1280,720))
        out_vid.write(im)
        #cv2.imshow("streaming", im)
        #cv2.waitKey(1)
        
