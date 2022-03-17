import glob
import os
import cv2
import time
import face_detection
import matplotlib.pyplot as plt
import numpy as np


def draw_faces(im, bboxes):
    for bbox in bboxes:
        x0, y0, x1, y1 = [int(_) for _ in bbox]
        cv2.rectangle(im, (x0, y0), (x1, y1), (0, 0, 255), 2)


if __name__ == "__main__":

    # vid = cv2.VideoCapture(0)
    # for i in range(120,1081,30):
    for i in [120,540,720,1080]:
        detector = face_detection.build_detector(
            "DSFDDetector",
            max_resolution=i
        )
        for batch in [1,2,4,8,16]:
            img = np.random.random((batch,1920,1080,3)).astype('uint8')
            t = time.time()
            for _ in range(10):
                dets = detector.detect(img[:, :, ::-1])
                # dets = detector.detect(img[:, :, ::-1])[:, :4]
            print(f"Detection time for {i} resolution,{batch} batch: {((time.time()- t)*1000)/10:.3f} milli_secs on device {detector.device}")

        print('-'*50)
    # cv2.imshow('img',img)
    # cv2.waitKey(0)


    # while(True):
    #     ret, frame = vid.read()
    #     re_frame = cv2.resize(frame,(1920,1080))
    #     # print(frame.shape)

    #     t = time.time()
    #     dets = detector.detect(re_frame[:, :, ::-1])[:, :4]
    #     print(f"Detection time: {time.time()- t:.3f}")


    #     draw_faces(re_frame, dets)

    #     cv2.imshow('frame', re_frame)
    #     if cv2.waitKey(1) & 0xFF == ord('q'):
    #         break

    # vid.release()
    # cv2.destroyAllWindows()





    # impaths = "images"
    # impaths = glob.glob(os.path.join(impaths, "*.jpg"))
    
    # for impath in impaths:
    #     if impath.endswith("out.jpg"): continue
    #     im = cv2.imread(impath)
    #     print("Processing:", impath)
    #     t = time.time()
    #     dets = detector.detect(
    #         im[:, :, ::-1]
    #     )[:, :4]
    #     print(f"Detection time: {time.time()- t:.3f}")
    #     draw_faces(im, dets)
    #     imname = os.path.basename(impath).split(".")[0]
    #     output_path = os.path.join(
    #         os.path.dirname(impath),
    #         f"{imname}_out.jpg"
    #     )

    #     cv2.imwrite(output_path, im)
        


# import cv2
  
  
# # define a video capture object
# vid = cv2.VideoCapture(0)
  
# while(True):
      
#     # Capture the video frame
#     # by frame
#     ret, frame = vid.read()
  
#     # Display the resulting frame
#     cv2.imshow('frame', frame)
      
#     # the 'q' button is set as the
#     # quitting button you may use any
#     # desired button of your choice
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
  
# # After the loop release the cap object
# vid.release()
# # Destroy all the windows
# cv2.destroyAllWindows()