import cv2
import numpy as np

def count_ppl_on_img(link: str):
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
    cap = cv2.VideoCapture(link)
    success, image = cap.read()

    if success:
        frame = cv2.resize(image, (640, 480))
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

        # detect people in the image
        # returns the bounding boxes for the detected objects
        boxes, weights = hog.detectMultiScale(frame, winStride=(8, 8))
    else:
        return 'Błąd'

    cap.release()
    cv2.destroyAllWindows()
    return len(boxes)



