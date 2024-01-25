import cv2


def show_camera():
    cap = cv2.VideoCapture(0)
    while True:  # Use the default camera (change if multiple cameras are available)    while (True):
        retu, frame0 = cap.read()
        cv2.imshow('frame', frame0)
        if cv2.waitKey(1) & 0xFF == ord('a'):
            break
    cap.release()
    cv2.destroyAllWindows()
