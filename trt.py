from face_detection.retinaface.tensorrt_wrap import TensorRTRetinaFace

inference_imshape =(480, 640) # Input to the CNN
input_imshape = (1080, 1920) # Input for original video source
detector = TensorRTRetinaFace(input_imshape, imshape)
boxes, landmarks, scores = detector.infer(image)

