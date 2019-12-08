import cv2

fn = r"../parking/data/test.mp4"
cap = cv2.VideoCapture(0)
count = 0 # imwrite의 frame count 
frame_path = "./parking/data/frame/"
if cap.isOpened():
	print('width: {}, height : {}'.format(cap.get(3), cap.get(4)))
	
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
cv2.destroyAllWindows()