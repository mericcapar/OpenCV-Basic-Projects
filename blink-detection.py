import cv2 
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector
from cvzone.PlotModule import LivePlot
import mediapipe as mp 


cap = cv2.VideoCapture(0)
detector = FaceMeshDetector()
plotY = LivePlot(640,360,[20,50])

idList = [22 , 23 , 24 , 26 , 110 , 157 , 158 , 159 , 160 , 161 , 130 , 243] # Important dots of eye. 
ratioList = []

blinkCounter = 0
dl = 0 
color = (255 , 0 ,255)



while True:
    _ , img = cap.read()
    
    img , faces = detector.findFaceMesh(img , draw = False)

    if faces:
        face = faces[0]
        for id in idList:
            cv2.circle(img , face[id] , 5 , color , cv2.FILLED )

        leftUp = face[159] #Location of left top eye
        leftDown = face[23] # Location of left down eye
        leftLeft = face[130]
        leftRight = face[243]
        
        lenghtVer , _ = detector.findDistance(leftUp , leftDown) #Distance between top and bottom of eye
        lenghtHor , _ = detector.findDistance(leftLeft , leftRight) #Distance between left and a right of eye

        cv2.line(img ,leftUp ,leftDown , (0, 200 , 0) , 3 )
        cv2.line(img ,leftLeft ,leftRight , (0, 200 , 0) , 3 )

        ratio = int((lenghtVer / lenghtHor) * 100) #With this line of code, even between person and camera changes, we can use same code.
        ratioList.append(ratio)

        if len(ratioList) > 3:
            ratioList.pop(0)

        ratioAvg = sum(ratioList) / len(ratioList)

        if ratioAvg < 35 and dl == 0:
            blinkCounter+=1
            color = (0 , 200 , 0)
            dl =1
        elif ratioAvg > 35:
            dl = 0
            color = (255 , 0 , 255)
        
        imgPlot = plotY.update(ratioAvg, color)

        #cv2.imshow("imgPlot", imgPlot)
        
        img = cv2.resize(img , (640,360)) # We need to resize to stack the images. 
        imgStack = cvzone.stackImages([img,imgPlot] , 2 , 1)
        cv2.putText(imgStack, f'Blink Counter: {blinkCounter}' , (10,30), cv2.FONT_HERSHEY_PLAIN , 2 , color , 3)
    else:
        img = cv2.resize(img , (640,360)) # We need to resize to stack the images. 
        imgStack = cvzone.stackImages([img,img] , 2  , 1)


    cv2.imshow('Stacked Image',imgStack)
    cv2.waitKey(50)
