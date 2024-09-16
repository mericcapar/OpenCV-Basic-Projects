import mediapipe as mp
import cv2
import time

cap = cv2.VideoCapture(0)

mpHand = mp.solutions.hands
hands = mpHand.Hands(max_num_hands = 2)

mpDraw = mp.solutions.drawing_utils

while True:

    _ , img = cap.read()
    imgRGB = cv2.cvtColor(img , cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    lmList = []

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(img , handLms , mpHand.HAND_CONNECTIONS)

        for id, lm in enumerate(handLms.landmark):
            h , w , _ = img.shape
            cx , cy = int(lm.x * w) , int(lm.y * h)
            lmList.append([id,cx,cy])
        
        if len(results.multi_hand_landmarks) == 1 and lmList:
            if(lmList[10][2] > lmList[6][2] and lmList[11][2] > lmList[7][2] and lmList[12][2] > lmList[8][2] and lmList[12][1] < lmList[8][1] and lmList[11][1] < lmList[7][1] and lmList[10][1] > lmList[6][1]):
                 cv2.putText(img , "Meric Nisayi seviyor" , (25 , 100) , cv2.FONT_HERSHEY_SIMPLEX , 3 , (255 , 0 , 255) , 5)
        if len(results.multi_hand_landmarks) == 2 and lmList:
            if(lmList[10][2] > lmList[6][2] and lmList[11][2] > lmList[7][2] and lmList[12][2] > lmList[8][2] and lmList[12][1] < lmList[8][1] and lmList[11][1] < lmList[7][1] and lmList[10][1] > lmList[6][1]):   
                cv2.putText(img , "Meric cok Nisayi seviyor" , (25 , 100) , cv2.FONT_HERSHEY_SIMPLEX , 3 , (255 , 0 , 255) , 5)



    cv2.imshow('img',img)
    cv2.waitKey(1)