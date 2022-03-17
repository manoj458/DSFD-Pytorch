from pathlib import Path
import re
import sys
import os
os.environ["CUDA_VISIBLE_DEVICES"]="0"
import subprocess
import os.path
from os import path
import threading
import datetime
import glob
import cv2
import time
import face_detection
#from face_detection.retinaface.tensorrt_wrap import TensorRTRetinaFace
import datetime
import http.client
import json
import shutil
import requests
import json
def split(a, n):
    k, m = divmod(len(a), n)
    return (a[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n))

def draw_faces(im, bboxes):
    for bbox in bboxes:
        x0, y0, x1, y1 = [int(_) for _ in bbox]
        cv2.rectangle(im, (x0, y0), (x1, y1), (0, 0, 255), 2)

def setEndDateAndTime(url,date):
    headers = {"Content-Type": "application/json",
                'Authorization': 'bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjYxYzU2ZTE2Yjk1NjYwMDAwZWE4Mzk5OSIsImlhdCI6MTY0MDM0NTAxNCwiZXhwIjoxNjQyOTM3MDE0fQ.e2oZTjLDG1QApGKLLYQtMBNjrORPyE818xztzZ6Gthc'}
    payload=  { "blurring_end_time": date}
    json_payload= json.dumps(payload)
    response = requests.put(url,data=json_payload, headers=headers)
    print(response.content)

def setBluredVideoPath(url, path):#    url1 = "http://192.168.1.164:4200/faceblurrings"
    headers = {"Content-Type": "application/json",
                'Authorization': 'bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjYxYzU2ZTE2Yjk1NjYwMDAwZWE4Mzk5OSIsImlhdCI6MTY0MDM0NTAxNCwiZXhwIjoxNjQyOTM3MDE0fQ.e2oZTjLDG1QApGKLLYQtMBNjrORPyE818xztzZ6Gthc'}
    payloadR=  {"blurred_video": path}
    json_payload= json.dumps(payloadR)
    response = requests.put(url,data=json_payload, headers=headers)#auth=('rajiv.N', 'Linoy@123'))
    print(response.content)

def setCompletedVideoPath(url, path):#    url1 = "http://192.168.1.164:4200/faceblurrings"
    headers = {"Content-Type": "application/json",
                'Authorization': 'bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjYxYzU2ZTE2Yjk1NjYwMDAwZWE4Mzk5OSIsImlhdCI6MTY0MDM0NTAxNCwiZXhwIjoxNjQyOTM3MDE0fQ.e2oZTjLDG1QApGKLLYQtMBNjrORPyE818xztzZ6Gthc'}
    payloadR=  {"completed_video": path}
    json_payload= json.dumps(payloadR)
    response = requests.put(url,data=json_payload, headers=headers)#auth=('rajiv.N', 'Linoy@123'))
    print(response.content)

def setStartDateAndTime(url,date):#    url1 = "http://192.168.1.164:4200/faceblurrings"
    headers = {"Content-Type": "application/json",
                'Authorization': 'bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjYxYzU2ZTE2Yjk1NjYwMDAwZWE4Mzk5OSIsImlhdCI6MTY0MDM0NTAxNCwiZXhwIjoxNjQyOTM3MDE0fQ.e2oZTjLDG1QApGKLLYQtMBNjrORPyE818xztzZ6Gthc'}
    payloadR=  {"blurring_initiation_time": date}
    json_payload= json.dumps(payloadR)
    response = requests.put(url,data=json_payload, headers=headers)#auth=('rajiv.N', 'Linoy@123'))
    print(response.content)


def checkIfCompleted(data):
    #completed= (data[0]['blurring_end_time'])
    if 'blurring_end_time' not in data:
        return False
    else:
        print("***File Already exist***")
        return True

def getPostUrlFromPath(path):
    print("Get Call"+path)
    URL = "http://192.168.1.164:4200/faceblurrings"
    PARAMS = {'path':path}
    r= requests.get(url = URL, params = PARAMS)
    data = r.json()
    if not data:
        return
    skip=checkIfCompleted(data)
    id=(data[0]['_id'])
    #print(data[0]['_id'])
    url= URL+'/'+id
    if url:
        print(url)
    return url, skip

def setCorrupted():
    headers = {"Content-Type": "application/json",
                'Authorization': 'bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjYxYzU2ZTE2Yjk1NjYwMDAwZWE4Mzk5OSIsImlhdCI6MTY0MDM0NTAxNCwiZXhwIjoxNjQyOTM3MDE0fQ.e2oZTjLDG1QApGKLLYQtMBNjrORPyE818xztzZ6Gthc'}
    payloadR=  {"file_corrupted": True}
    json_payload= json.dumps(payloadR)
    response = requests.put(url,data=json_payload, headers=headers)#auth=('rajiv.N', 'Linoy@123'))
    print(response.content)


def storeAllPath(cur_path):
    pathList=[]
    for path in Path(cur_path).rglob('*.dat'):
     #   print(path.name)
        pathP = str(path.parent)+'/' + str(path.name)
        #print(pathP)
        pathList.append(pathP)
    return pathList

def decryptVideo(nputFile):
    inputFile= str(sys.argv[1])
    outputFile=inputFile[:-4]
    print (outputFile)
    subprocess.call(['openssl', 'smime', '-decrypt', '-in='+ inputFile, '-binary', '-inform', 'DER','-inkey=private-key.pem', '-out='+outputFile])
    print("File Decrypted Successfully")
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
pathList=storeAllPath(ip_dir)
#op_dirBlured = ( ip_dir[:-1]+"_Face_Blured/")
#op_dir = ( "Face_Blur"+"/"+ip_dir)
datestring = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
#os.makedirs(op_dir, exist_ok=True)
#total_ip_files = os.listdir(ip_dir)
total_ip_files = storeAllPath(ip_dir)
print("tota files:" +str(len(total_ip_files)))
ip_split = list(split(total_ip_files, 5))
ip_files       = ip_split[0]
ip_files1      = ip_split[1] #total_ip_files[len(total_ip_files)/3 : 2 * len(total_ip_files)/3]
ip_files2      = ip_split[2] #total_ip_files[2 * len(total_ip_files)/3 : ]
ip_files3      = ip_split[3]#total_ip_files[2 * len(total_ip_files)/3 : ]
ip_files4      = ip_split[4] #total_ip_files[2 * len(total_ip_files)/3 : ]
#pathUrl ="/data/videos/DPW/dev009/cam8/001.mp4" 
#url= getPostUrlFromPath(pathUrl)
#setStartDateAndTime(url,datestring)
#
#sys.exit("Execute Later")
#print()i
def launch(detector, ip_files):
    for filename in ip_files:
        op_dirBlured = ( op_dir+"/Face_Blured/")
        #print("op_dir#")
        print("output Directory:    " + op_dirBlured)
        file_path = os.path.join(ip_dir, filename)
        print("File Path:    " + file_path)
        outputFile=file_path[:-4]
        subprocess.call(['openssl', 'smime', '-decrypt', '-in='+ file_path, '-binary', '-inform', 'DER','-inkey=private-key.pem', '-out='+outputFile])
        sys.exit("Execute Later")
        sys.exit("Execute Later")
        url, skip = getPostUrlFromPath(file_path)
        #pathUrl ="/data/videos/DPW/dev002/cam2/001.mp4" 
        dateString = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
        setStartDateAndTime(url, dateString)
        #sys.exit("Checking get ca`:qll")
        print("File_Path:     "+file_path)
        if skip == True:
            print("c")
            continue
        cap = cv2.VideoCapture(file_path)
        #print("cap initiated") 
        if cap.isOpened() == False:
            print("Coudn't open video file. Marking it as corrupted")
            #setCorrupted()
            continue
        #fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        #print("Hey")
        #fileWriteName=file_path[:-4]+"B.avi"
        print("Destination path:    "+(op_dirBlured+filename[6:-7]))
        op_dirBlured= op_dirBlured+filename[6:-7]
        os.makedirs(op_dirBlured, exist_ok=True)
        print("Filename Var:    "+ filename[47:-4])
        outputFileName= filename[22:-4]+ ".mp4"
        print("outputFileName:  "+outputFileName)
        print("outputFileName+ dir:  "+op_dirBlured+outputFileName)
        setBluredVideoPath(url,(op_dirBlured+outputFileName))
        out_vid = cv2.VideoWriter(os.path.join(op_dirBlured,outputFileName), fourcc, 30.0, (1280,720))
        #out_vid = cv2.VideoWriter(os.path.join(op_dir,filename), fourcc, 30.0, (1280,720))

        print("initiating blurring for video", filename)

        while True:

            ret, im = cap.read()
      
            if ret == False:
                print("ret is false")
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
            im = cv2.resize(im, (1280,720))
            out_vid.write(im)
        endTimeString = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
        setEndDateAndTime(url,endTimeString)
        #completedPath = ip_dir[:-1]+"_Completed_Face_Blur/"
        completedPath = "/data1/"+"Completed_Face_Blur/"
        completedPath= completedPath+filename[13:-7]
        os.makedirs(completedPath, exist_ok=True)
        print("Completed path:  "+ completedPath)
        #print(file_path)
        setCompletedVideoPath(url,completedPath)
        #shutil.move(file_path,completedPath )
        #os.remove(file_path)

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


