import mediapipe as mp
import cv2 
import math 
import numpy as np

#We need to calculate the angle of 11, 13 ,15 positions for push-up detection.
def findAngle (img , p1 , p2 ,p3 , lmList , draw = True): 
    #We dont need ID so we only get x and y positions.
    x1 , y1 = lmList[p1][1:]  
    x2 , y2 = lmList[p2][1:] 
    x3 , y3 = lmList[p3][1:] 

    #Calculating the angle

    #We can calculate the angle with this way.
    angle = math.degrees(math.atan2( y3 - y2 , x3 - x2 ) - (math.atan2( y1 - y2 , x2- x1 ))) 

    if angle < 0 : 
        angle += 360 #The angle should be positive for easier calculation.

    if draw:
        cv2.line(img , (x1 , y1) , (x2, y2) , (0 , 255 , 255) , 8)
        cv2.line(img , (x3 , y3) , (x2, y2) , (0 , 255 , 255) , 8)

        cv2.circle(img , (x1,y1) , 20 , (0 , 255 , 255) , cv2.FILLED)
        cv2.circle(img , (x2,y2) , 20 , (0 , 255 , 255) , cv2.FILLED)
        cv2.circle(img , (x3,y3) , 20 , (0 , 255 , 255) , cv2.FILLED)

        cv2.circle(img , (x1,y1) , 30 , (0 , 255 , 255))
        cv2.circle(img , (x2,y2) , 30 , (0 , 255 , 255))
        cv2.circle(img , (x3,y3) , 30 , (0 , 255 , 255))

        cv2.putText(img , str(int(angle)) , (x2+40 , y2+40) , cv2.FONT_HERSHEY_SIMPLEX , 3 , (0,255 , 255) , 3)
    return angle
        


cap = cv2.VideoCapture('push-ups3.mp4')


mpPose = mp.solutions.pose
pose = mpPose.Pose()

mpDraw = mp.solutions.drawing_utils

dir = 1
count = 0

landmark_spec = mpDraw.DrawingSpec(color=(0, 0, 255), thickness=6, circle_radius=5) # Better visual for lines
connection_spec = mpDraw.DrawingSpec(color=(255, 255, 255), thickness=5, circle_radius=5) # Better visual for dots

while True:
    sucess , img = cap.read()
    
    imgRGB = cv2.cvtColor(img , cv2.COLOR_BGR2RGB)

    results = pose.process(imgRGB)

    lmList = [] #We will add dots locations to this list. 
    if results.pose_landmarks:
        mpDraw.draw_landmarks(img , results.pose_landmarks, mpPose.POSE_CONNECTIONS , landmark_spec , connection_spec)

        for id , lm in enumerate(results.pose_landmarks.landmark):
            h , w , _ = img.shape
            cx , cy = int(lm.x * w) , int(lm.y * h )
            lmList.append([id , cx , cy]) #Adding dots locations to list
    
    if len(lmList) != 0:

        angle = findAngle(img , 11 , 13 ,15 , lmList )
        per = np.interp(angle , (140 , 162) , (0 , 100 ))
        #print(angle)

        if per == 100: #If started the push-up and if he's down
            if dir == 0:
                count += 0.5
                dir = 1
        
        if per == 0: #If he was down and he goes up. 
            if dir == 1:
                count += 0.5
                dir =0

        print(count)

        cv2.putText( img , 'Sinav Sayisi: ' + str(int(count)) , ( 25, 125) , cv2.FONT_HERSHEY_SIMPLEX , 5 , (255,0,0) , 5)
    




        






    cv2.imshow('Push Up Counter' , img)
    cv2.waitKey(20)

    #if cv2.waitKey(1) & 0xFF == 27:
     #   break

#cap.release()
#cv2.destroyAllWindows()
