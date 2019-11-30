import cv2
import numpy as np

video_path = 'test.mp4'  #비디오 경로 설정
cap = cv2.VideoCapture(video_path) #동영상 로드

#output_size = (187, 333) # (width, height)

#fourcc = cv2.VideoWriter_fourcc('m','p','4','v')
#out = cv2.VideoWriter('%s_output.mp4' % (video_path.split('.')[0]), fourcc, cap.get(cv2.CAP_PROP_FPS))
                        #이 파일의 이름으로 저장을 해라                 #코덱   #FPS = 불러온 동영상 Frame만큼  

#동영상이 제대로 열렸는지 확인 -> Not이면 exit()
if not cap.isOpened():
    exit() 

#오브젝트 트래커
tracker = cv2.TrackerCSRT_create()

ret, img = cap.read()
cv2.namedWindow('Select Window')
cv2.imshow('Select Window', img)

# setting ROI
rect = cv2.selectROI('Select Window', img, fromCenter=False, showCrosshair=True)
cv2.destroyWindow('Select Window')

# initailize tracker
tracker.init(img, rect) # rect로 설정한 부분을 tracking

while True:
    ret, img = cap.read() #동영상 1프레임씩 읽어오는 함수

    if not ret:
        exit()

    success, box = tracker.update(img) #img에서 rect로 설정한 이미지와 비슷한 물체의 위치를 찾아 반환

    left, top, w, h = [int(v) for v in box] #박스에서 나오는 위치값을 저장
    
    #center_x = left + w / 2
    #center_y = top + h / 2
    #result_top = int(center_y - output_size[1] / 2)
    #result_bottom = int(center_y + output_size[1] / 2)
    #result_left = int(center_x - output_size[1] / 2)
    #result_right = int(center_x + output_size[1] / 2)

    #result_img = img[result_top:result_bottom, result_left:result_right]

    #사각형 setting
    cv2.rectangle(img, pt1=(left, top), pt2=(left + w, top + h), color=(255,255,255), thickness=2)


    cv2.imshow('img', img)  #윈도우에 이미지 출력
    if cv2.waitKey(1) == ord('q'):
        break               #Q를 입력시 while문 braek함



