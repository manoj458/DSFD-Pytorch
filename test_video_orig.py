import sys
import os
os.environ["CUDA_VISIBLE_DEVICES"]="0"
import threading
import datetime
import glob
import cv2
import time
import face_detection
#from face_detection.retinaface.tensorrt_wrap import TensorRTRetinaFace
import datetime
import http.client
def split(a, n):
    k, m = divmod(len(a), n)
    return (a[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n))

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
        max_resolution=720
    )
    detector1 = face_detection.build_detector(
        "DSFDDetector",
        #"RetinaNetResNet50",
        #"RetinaNetMobileNetV1",
        max_resolution=720
    )
    detector2 = face_detection.build_detector(
        "DSFDDetector",
        #"RetinaNetResNet50",
        #"RetinaNetMobileNetV1",
        max_resolution=720
    )
    detector3 = face_detection.build_detector(
        "DSFDDetector",
        #"RetinaNetResNet50",
        #"RetinaNetMobileNetV1",
        max_resolution=720
    )
    detector4 = face_detection.build_detector(
        "DSFDDetector",
        #"RetinaNetResNet50",
        #"RetinaNetMobileNetV1",
        max_resolution=720
    )

if len(sys.argv)!=3:
   sys.exit("Incorrect arguments!")

ip_dir = sys.argv[1]
op_dir = sys.argv[2]
datestring = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
op_dir = os.path.join(op_dir, str("faceblur_" + datestring))
if os.path.exists(op_dir) is False:
   os.mkdir(op_dir)
total_ip_files = os.listdir(ip_dir)
ip_split = list(split(total_ip_files, 5))
ip_files       = ip_split[0]
ip_files1      = ip_split[1] #total_ip_files[len(total_ip_files)/3 : 2 * len(total_ip_files)/3]
ip_files2       = ip_split[2] #total_ip_files[2 * len(total_ip_files)/3 : ]
ip_files3       = ip_split[3] #total_ip_files[2 * len(total_ip_files)/3 : ]
ip_files4       = ip_split[4] #total_ip_files[2 * len(total_ip_files)/3 : ]
def launch(detector, ip_files):
    print(ip_files)
    for filename in ip_files:
        file_path = os.path.join(ip_dir, filename)
        cap = cv2.VideoCapture(file_path)
    
        if cap.isOpened() == False:
            continue

        out_vid = cv2.VideoWriter(os.path.join(op_dir,filename), cv2.VideoWriter_fourcc('M','P','4','V'), 30.0, (1280, 720))

        print("initiating blurring for video", filename)

        while True:

            ret, im = cap.read()
      
            if ret == False:
                break 
            h, w, c = im.shape
            t = time.time()
            dets = detector.detect(
            im[:, :, ::-1]
        )[:, :4]
            print(f"Detection time: {time.time()- t:.3f}")

            for bbox in dets:
                x0, y0, x1, y1 = [int(_) for _ in bbox]
                if x0<0:
                    x0 = 0
                if y0<0:
                    y0 = 0
                if x0>w:
                    x0 = w-1
                if y0>h:
                    y0 = h-1
                if x1<0:
                    x1 = 1
                if y1<0:
                    y1 = 1
                if x1>w:
                    x1 = w
                if y1>h:
                    y1 = h
                #print(x0,y0,x1,y1)
                sub_face = im[y0:y1, x0:x1]
                sub_face = cv2.GaussianBlur(sub_face,(23, 23), 30)
                if sub_face is None:
                    continue
                im[y0:y0+sub_face.shape[0], x0:x0+sub_face.shape[1]] = sub_face
            im = cv2.resize(im, (1280, 720))
            out_vid.write(im)

t1 = threading.Thread(target=launch, args=(detector,ip_files))
t2 = threading.Thread(target=launch, args=(detector1,ip_files1))
t3 = threading.Thread(target=launch, args=(detector2,ip_files2))
t4 = threading.Thread(target=launch, args=(detector3,ip_files3))
t5 = threading.Thread(target=launch, args=(detector4,ip_files4))

t1.start()
t2.start()
t3.start()
t4.start()
t5.start()

t1.join()
t2.join()
t3.join()
t4.join()
t5.join()
