import cv2
import mediapipe as mp
import math
import numpy as np

def findAngle(video, p1 , p2 ,p3 , lmList , draw = True):
    x1 , y1 = lmList[p1][1:]
    x2 , y2 = lmlist[p2][1:]
    x3 , y3 = lmList[p3][1:]

    angle = math.degrees(math.atan2( y3 - y2 , x3 - x2 ) - (math.atan2( y1 - y2 , x2- x1 ))) 
    
    if angle < 0:
        angle +=360

    if draw:
        cv2.line(video , (x1 , y1) , (x2 , y2) , (255 , 255 , 0) , 8)
        cv2.line(video , (x3 , y3) , (x2 , y2) , (255 , 255 , 0) , 8)

        cv2.circle(video , (x1 , y1) , 20 , (0 , 255 ,255) , cv2.FILLED)
        cv2.circle(video , (x2 , y2) , 20 , (0 , 255 ,255) , cv2.FILLED)
        cv2.circle(video , (x3 , y3) , 20 , (0 , 255 ,255) , cv2.FILLED)

        cv2.circle(video , (x1 , y1) , 30 , (0 , 255 ,255))
        cv2.circle(video , (x1 , y1) , 30 , (0 , 255 ,255))
        cv2.circle(video , (x1 , y1) , 30 , (0 , 255 ,255))

        cv2.putText(video , str(int(angle)) , (x2+40 , y2+40) , cv2.FONT_HERSHEY_SIMPLEX , 3 , (0,255 , 255) , 3)
    return angle

cap = cv2.VideoCapture('curl1.mp4')

mpPose = mp.solutions.pose
pose = mpPose.Pose()

mpDraw = mp.solutions.drawing_utils

landmark_spec = mpDraw.DrawingSpec(color=(0, 0, 255), thickness=6, circle_radius=5) # Better visual for lines
connection_spec = mpDraw.DrawingSpec(color=(255, 255, 255), thickness=5, circle_radius=5) # Better visual for dots

dir = 1
count = 0

while True:
    success , video = cap.read()
    videoRGB = cv2.cvtColor(video , cv2.COLOR_BGR2RGB)

    results = pose.process(videoRGB)

    lmlist = []

    if results.pose_landmarks:
        #mpDraw.draw_landmarks(video , results.pose_landmarks , mpPose.POSE_CONNECTIONS , landmark_spec , connection_spec)

        for id, lm in enumerate(results.pose_landmarks.landmark):
            h , w , _ = video.shape
            cx , cy = int(lm.x * w) , int(lm.y * h)

            lmlist.append([id , cx ,cy ])

    if len(lmlist) != 0:

        angle = findAngle(video , 11 , 13 ,15 , lmlist)

        per = np.interp(angle , (250 , 300) , (0 , 100))


        if per == 100:
            if dir ==0:
                count += 0.5
                dir =1
            
        if per == 0:
            if dir == 1:
                count += 0.5
                dir = 0

        print(count)

        cv2.putText(video , 'Curl Sayisi : ' + str(int(count)) , (50 , 150) , cv2.FONT_HERSHEY_SIMPLEX , 5 , (255,0,255) , 5)


    cv2.imshow('video' , video)
    cv2.waitKey(15)