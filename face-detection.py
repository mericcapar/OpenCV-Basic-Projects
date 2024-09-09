import cv2
import mediapipe as mp 


cap = cv2.VideoCapture('face2.mp4')


mpFaceDetection = mp.solutions.face_detection

faceDecetion = mpFaceDetection.FaceDetection(0.20)  #you can input data in this field between 0 and 1. It will make the detection more sensitive or easier.
#If you make it so low, it can detect everything as a face and if you make it so sensitive it will be pretty hard to find anything

mpDraw = mp.solutions.drawing_utils


while True:
    sucess , img = cap.read()
    imgRGB =  cv2.cvtColor(img , cv2.COLOR_BGR2RGB)
    results = faceDecetion.process(imgRGB)
    #print(results.detections)

    if results.detections:
        for id , detection in enumerate(results.detections):
            bBoxC = detection.location_data.relative_bounding_box #bounding box 
            # print(bBoxC) # we will get the shape of the box with results of bBoxC, results are xmin , ymin, width and height
            h , w , _ = img.shape
            bbox = int(bBoxC.xmin * w) , int(bBoxC.ymin * h) , int(bBoxC.width * w) , int(bBoxC.height * h)
            #print(bbox) #We can see the corners of the boxes.

            cv2.rectangle(img , bbox , (0,255,255) , 2)





    cv2.imshow('img' , img)
    cv2.waitKey(10) 
