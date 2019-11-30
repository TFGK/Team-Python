import pickle
import numpy as np
import cv2

fn_out = r"/test.mp4"
fn_data = r"/config.pkl"
config = {'save_video': False,
          'text_overlay': True,
          'parking_overlay': True,
          'parking_id_overlay': False,
          'parking_detection': True,
          'min_area_motion_contour': 60,
          'park_sec_to_wait': 3,
          'start_frame': 0} #35000

# 공간 저장된 data 로드
with open(fn_data, 'r') as stream:
    parking_data = pickle.load(stream)
print(stream)


# Set capture device or file
cap = cv2.VideoCapture(0)

# print cap.get(5) 
video_info = {'fps':    cap.get(cv2.CAP_PROP_FPS),
              'width':  int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
              'height': int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
              'fourcc': cap.get(cv2.CAP_PROP_FOURCC),
              'num_of_frames': int(cap.get(cv2.CAP_PROP_FRAME_COUNT))}
cap.set(cv2.CAP_PROP_POS_FRAMES, config['start_frame']) # jump to frame

# Define the codec and create VideoWriter object
if config['save_video']:
    fourcc = cv2.VideoWriter_fourcc('M','P','4','V')
    out = cv2.VideoWriter(fn_out, -1, 25.0, #video_info['fps'], 
                          (video_info['width'], video_info['height']))


    


#마우스 이벤트 콜백함수 정의
def mouse_callback(event, x, y, flags, param): 
    print("마우스 이벤트 발생, x:", x ," y:", y) # 이벤트 발생한 마우스 위치 출력
    points = np.zeros((256, 256, 3), np.uint8)  # 행렬 생성, (가로, 세로, 채널(rgb)),bit)

cv2.namedWindow('image')  #마우스 이벤트 영역 윈도우 생성
