import cv2 
import mediapipe as mp
import time

#How meshing works?
#First it crops the face and make feature extractor. The futures are eye, lips and other face things. In the end it concatenes the dots

cap = cv2.VideoCapture('face-mesh2.mp4')

mpFaceMesh = mp.solutions.face_mesh
faceMesh = mpFaceMesh.FaceMesh(max_num_faces = 1)

mpDraw = mp.solutions.drawing_utils
drawSpec = mpDraw.DrawingSpec(thickness = 1 , circle_radius = 1)

while True:
    success , img = cap.read()
    imgRGB = cv2.cvtColor(img , cv2.COLOR_BGR2RGB)

    results = faceMesh.process(imgRGB)
    print(results.multi_face_landmarks)

    if results.multi_face_landmarks:
        for faceLms in results.multi_face_landmarks:
            mpDraw.draw_landmarks(img , faceLms , mpFaceMesh.FACEMESH_TESSELATION, drawSpec , drawSpec) #FACEMESH_CONTOURS

        for id , lm in enumerate(faceLms.landmark):
            h , w , _ = img.shape
            cx , cy = int(lm.x*w) , int(lm.y * h) 
            print([id , cx , cy])






    cv2.imshow('img', img)
    cv2.waitKey(10)