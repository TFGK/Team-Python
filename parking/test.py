import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import cv2
import imutils
import numpy as np
import yaml

index = 1 #저장 index 카운트
list_data = [] #pts를 묶는 배열
# 공간 좌표 저장 배열
pts = []  #튜플 저장공간
pts2 = [] #배열
fn = r"../parking/data/test.mp4"
fn_yaml = r"../parking/data/parking_sapce_data.yml"
fn_out = r"../parking/data/output.avi"
config = {
	'save_video': False,
    'text_overlay': True,
    'parking_overlay': True,
	'parking_id_overlay': False,
    'parking_detection': True,
    'min_area_motion_contour': 60,
    'park_sec_to_wait': 3,
    'start_frame': 0
}

class test(QMainWindow):
    def __init__(self): 
        super().__init__()      #상위객체 생성 및 호출
        self.initUI()
    
    def initUI(self):           #기본 UI
        self.statusBar()
        self.statusBar().showMessage('test')

        pybutton = QPushButton('화면 캡처', self)
        pybutton.resize(100, 32)
        pybutton.move(10, 20)
        #클릭 이벤트 연결
        pybutton.clicked.connect(self.capture)

        pybutton = QPushButton('공간 지정', self)
        pybutton.resize(100, 32)
        pybutton.move(130, 20)
        #클릭 이벤트 연결
        pybutton.clicked.connect(self.space)

        pybutton = QPushButton('메인 실행', self)
        pybutton.resize(100, 32)
        pybutton.move(250, 20)
        #클릭 이벤트 연결
        pybutton.clicked.connect(self.parking)
    
        self.setGeometry(700, 400, 400, 80)
        self.setWindowTitle('공간 인식')
        self.show()             
    
    def closeEvent(self, QCloseEvent):
        ans = QMessageBox.question(self, "종료 확인", "종료하시겠습니까?",
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if ans == QMessageBox.Yes:
            QCloseEvent.accept()
        else:
            QCloseEvent.ignore()
    

    #공간 지정 함수
    def space(self):
        # 이미지창 생성 및 함수실행
        img = cv2.imread("./frame0.jpg")

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
            cv2.destroyWindows()
        ###와일끝
    
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

    #사진 캡처 함수
    def capture(self):
        cap = cv2.VideoCapture(fn)
        count = 0 # imwrite frame count 
        frame_path = "./parking/data/frame/"
        if cap.isOpened():
            print('width: {}, height : {}'.format(cap.get(3), cap.get(4)))
            print('저장 : S , // 종료 : Q')
        while True:
            ret, fram = cap.read()
            if ret:
                gray = cv2.cvtColor(fram, cv2.COLOR_BGR2GRAY)
                cv2.imshow('video', gray)

                k = cv2.waitKey(1) & 0xFF 
                if k == ord('q'):
                    break
                if k == ord('s'):
                    cv2.imwrite('frame%d.jpg' % count, fram)
                    print('saved frame%d.jpg' % count)
                    count += 1
            else:
                print('error')
        cap.release()
        cv2.destroyWindow()

    #실행
    def parking(self):
        #동영상 프레임 캡쳐
        cap = cv2.VideoCapture(fn)
        video_info = {
            'fps':    cap.get(cv2.CAP_PROP_FPS),
            'width':  int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            'height': int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            'fourcc': cap.get(cv2.CAP_PROP_FOURCC),
            'num_of_frames': int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        }
        cap.set(cv2.CAP_PROP_POS_FRAMES, config['start_frame']) # jump to frame

        # 코덱 정의 및 VideoWriter 객체 생성
        if config['save_video']:
            fourcc = cv2.VideoWriter_fourcc('m','p','4','x')# options: ('P','I','M','1'), ('D','I','V','X'), ('M','J','P','G'), ('X','V','I','D')
            out = cv2.VideoWriter(fn_out, -1, 25.0, #video_info['fps'], 
            (video_info['width'], video_info['height']))

        #YAML 데이터 읽기 (주차 공간)
        with open(fn_yaml, 'r') as stream:
            parking_data = yaml.load(stream)
        parking_contours = []           #윤곽(같은 값을 가진곳을 연결) 등고선, 등압선 등
        #openCV에서 Contour 찾기는 검정색 배경에서 흰색 물체를 찾아야함. 대상은 흰색, 배경은 검정색으로 변경해야한다.

        parking_bounding_rects = []     #윤곽의 사각형
        parking_mask = []
        for park in parking_data:
            points = np.array(park['points'])
            rect = cv2.boundingRect(points)     #points공간에 맞춰서 사각형 생성 -> rect 변수에 저장
            points_shifted = points.copy()
            points_shifted[:,0] = points[:,0] - rect[0] # 윤곽을 roi로 옮김
            points_shifted[:,1] = points[:,1] - rect[1]
            parking_contours.append(points)     #윤곽
            parking_bounding_rects.append(rect) 
            # parking bounding 배열 안에 rect를 어펜드
            #우리가 찾은 contour를 실제로 그리는 함수(5개의 파라미터) --> 즉 검은색 배경에 흰색 오브젝트처리
            # https://m.blog.naver.com/samsjang/220516697251 참조
            #cv2.drawContours(img, contours, -1, (0,255,0), 1)
            #img : contour를 나타낼 대상 이미지 /  contours : img에 그릴 contour / -1 : img에 실제로 그릴 인덱스파라미터 음수면 모든 contour를 그림
            #color : 선의 색상 / thickness : 선의 굵기

            mask = cv2.drawContours(np.zeros((rect[3], rect[2]), dtype=np.uint8), [points_shifted],
                                    contourIdx=-1, color=255, thickness=-1, lineType=cv2.LINE_8)
            mask = mask==255
            parking_mask.append(mask)

        parking_status = [False]*len(parking_data)
        parking_buffer = [None]*len(parking_data)


        #주차공간 on off 부분인데 이해 아직 못했음
        while(cap.isOpened()):
            spot = 0
            occupied = 0 
            # Read frame-by-frame
            video_cur_pos = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0 # Current position of the video file in seconds
            video_cur_frame = cap.get(cv2.CAP_PROP_POS_FRAMES) # Index of the frame to be decoded/captured next
            ret, frame = cap.read()
            if ret == False:
                print("Capture Error")
                break

            # frame_gray = cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2GRAY)
            # Background Subtraction
            frame_blur = cv2.GaussianBlur(frame.copy(), (5,5), 3)
            frame_gray = cv2.cvtColor(frame_blur, cv2.COLOR_BGR2GRAY)
            frame_out = frame.copy()

            if config['parking_detection']:
                #인덱스와 park리스트
                for ind, park in enumerate(parking_data):
                    points = np.array(park['points'])
                    rect = parking_bounding_rects[ind]
                    roi_gray = frame_gray[rect[1]:(rect[1]+rect[3]), rect[0]:(rect[0]+rect[2])] # crop roi for faster calculation
                    # print np.std(roi_gray)
                    points[:,0] = points[:,0] - rect[0] # shift contour to roi
                    points[:,1] = points[:,1] - rect[1]
                    # print np.std(roi_gray), np.mean(roi_gray)
                    status = np.std(roi_gray) < 22 and np.mean(roi_gray) > 53
                    # 주차 상태 변화를 감지한 경우 -> 현재 시간 저장
                    # If detected a change in parking status, save the current time
                    if status != parking_status[ind] and parking_buffer[ind]==None:
                        parking_buffer[ind] = video_cur_pos
                    

                    # status가 저장된 상태와 다르고 카운터가 열려있는 경우
                    # If status is still different than the one saved and counter is open
                    elif status != parking_status[ind] and parking_buffer[ind]!=None:
                        if video_cur_pos - parking_buffer[ind] > config['park_sec_to_wait']:
                            parking_status[ind] = status
                            parking_buffer[ind] = None
                        

                    #상태가 동일하고 카운터가 열려있는 경우
                    # If status is still same and counter is open                    
                    elif status == parking_status[ind] and parking_buffer[ind]!=None:
                        #if video_cur_pos - parking_buffer[ind] > config['park_sec_to_wait']:
                        parking_buffer[ind] = None                    
                    # print(parking_status)
            if config['parking_overlay']:
                for ind, park in enumerate(parking_data):
                    points = np.array(park['points'])
                    if parking_status[ind]:
                        color = (0,255,0)
                        spot = spot+1
                    else:
                        color = (0,0,255)
                        occupied = occupied+1
                    cv2.drawContours(frame_out, [points], contourIdx=-1,
                        color=color, thickness=2, lineType=cv2.LINE_8)
                    moments = cv2.moments(points)
                    centroid = (int(moments['m10']/moments['m00'])-3, int(moments['m01']/moments['m00'])+3)
                    cv2.putText(frame_out, str(park['id']), (centroid[0]+1, centroid[1]+1), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255,255,255), 1, cv2.LINE_AA)
                    cv2.putText(frame_out, str(park['id']), (centroid[0]-1, centroid[1]-1), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255,255,255), 1, cv2.LINE_AA)
                    cv2.putText(frame_out, str(park['id']), (centroid[0]+1, centroid[1]-1), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255,255,255), 1, cv2.LINE_AA)
                    cv2.putText(frame_out, str(park['id']), (centroid[0]-1, centroid[1]+1), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255,255,255), 1, cv2.LINE_AA)
                    cv2.putText(frame_out, str(park['id']), centroid, cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0,0,0), 1, cv2.LINE_AA)
                    # print 'occupied: ', occupied
                    # print 'spot: ', spot

            # # Draw Overlay
            # if config['text_overlay']:
            #     cv2.rectangle(frame_out, (1, 5), (280, 90),(255,255,255), 85)
            #     str_on_frame = "Frames: %d/%d" % (video_cur_frame, video_info['num_of_frames'])
            #     cv2.putText(frame_out, str_on_frame, (5,30), cv2.FONT_HERSHEY_SCRIPT_COMPLEX,
            #         0.7, (0,128,255), 2, cv2.LINE_AA)
            #     str_on_frame = "Spot: %d Occupied: %d" % (spot, occupied)
            #     cv2.putText(frame_out, str_on_frame, (5,90), cv2.FONT_HERSHEY_SCRIPT_COMPLEX,
            #                     0.7, (0,128,255), 2, cv2.LINE_AA)
                                
            # write the output frame
            if config['save_video']:
                if video_cur_frame % 35 == 0: # take every 30 frames
                    out.write(frame_out)

            # Display video
            cv2.imshow('DetecÃ§Ã£o de Vagas de Estacionamento', frame_out)
            cv2.waitKey(10)
            #cv2.imshow('background mask', bw)
            k = cv2.waitKey(1)
            if k == ord('q'):
                break
            elif k == ord('c'):
                cv2.imwrite('frame%d.jpg' % video_cur_frame, frame_out)

        cap.release()
        if config['save_video']: out.release()
        cv2.destroyWindows()    

app = QApplication(sys.argv)    #어플리케이션 객체 생성
w = test()
sys.exit(app.exec_())