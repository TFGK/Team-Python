import cv2
import numpy as np

video_path = 'test_video.mp4'
cap = cv2.VideoCapture(video_path) #동영상을 로드하는 함수 cv2.videoCaputre() 

#동영상이 제대로 안열렸으면 프로그램을 종료한다
if not cap.isOpened():  
    exit()

while True:
    ret, img = cap.read() #동영상 1프레임씩 로드

    if not ret:         #동영상 재생이 끝나면 ret 변수가 홀수가 됨 -> 종료
        exit()
    cv2.imshow('img', img)
    if cv2.waitkey(1) == ord('q'):      #키 입력을 n밀리세컨드동안 기다림
        break
    