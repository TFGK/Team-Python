import cv2
import imutils
import numpy as np
import yaml

index = 1 #저장 index 카운트
list_data = [] #pts를 묶는 배열
# 공간 좌표 저장 배열
pts = []  #튜플 저장공간
pts2 = [] #배열

#mouse function
def draw_roi(event, x, y, flags, param):
    img2 = img.copy()

    if event == cv2.EVENT_LBUTTONDOWN:  # 좌클릭->배열에 x,y 저장
        pts.append((x, y)) #튜플로 저장돼서 저장이 안되더라
        pts2.append([x,y]) #그래서 새롭게 변수하나 더만들어서

    if event == cv2.EVENT_RBUTTONDOWN:  # 우클릭->뒤로가기
        pts.pop()

    if event == cv2.EVENT_MBUTTONDOWN:  # 점과 점사이
        mask = np.zeros(img.shape, np.uint8)
        points = np.array(pts, np.int32)
        points = points.reshape((-1, 1, 2))
        # 다각형 그리기
        mask = cv2.polylines(mask, [points], True, (255, 255, 255), 2) # 
        mask2 = cv2.fillPoly(mask.copy(), [points], (255, 255, 255))  # ROI를 구하는데 사용
        mask3 = cv2.fillPoly(mask.copy(), [points], (0, 255, 0))  # PC에 표시되는 그래픽

        show_image = cv2.addWeighted(src1=img, alpha=0.8, src2=mask3, beta=0.2, gamma=0)

        cv2.imshow("mask", mask2)
        cv2.imshow("show_img", show_image)

        ROI = cv2.bitwise_and(mask2, img)   #mask2 + img의 and 연산
        cv2.imshow("ROI", ROI)
        cv2.waitKey(0)

    if len(pts) > 0:
        # 마지막 점 선택
        cv2.circle(img2, pts[-1], 3, (0, 0, 255), -1)

    if len(pts) > 1:
        # 선 긋기
        for i in range(len(pts) - 1):
            #cv2.circle(이미지,중심좌표,반지름,RGB,선굵기)
            cv2.circle(img2, pts[i], 5, (0, 0, 255), -1)  # x,y 좌표 클릭
            cv2.line(img=img2, pt1=pts[i], pt2=pts[i + 1], color=(255, 0, 0), thickness=2)

    cv2.imshow('image', img2)

# 이미지창 생성 및 함수실행
img = cv2.imread("./data/image.jpg")
img = imutils.resize(img, width=500)

cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_roi)
print("[INFO] 좌클릭 : 점 선택, 우클릭 : 점 취소, S : ROI구역 확정&저장")
print("[INFO] 종료: Q")

while True:
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    if key == ord("s"):
        saved_data = dict(
            id = index,
            points = pts2
        )
        index += 1 #저장 횟수 카운트 증가
        list_data.append(saved_data) # 전체 배열에 추가
        print("[INFO] ROI저장 완료.")
    if key == ord("c"):
        # 배열 초기화
        pts = []  
        pts2 = []

#배열확인
with open(r"./data/parking_sapce_data.yml", 'w') as file:
    test = yaml.dump(list_data, file, default_flow_style=False)

print(list_data)
cv2.destroyAllWindows()



