import cv2


def draw_face_box(frame, region):
    x1, y1, w, h = region["x"], region["y"], region["w"], region["h"]
    x2, y2 = x1 + w, y1 + h
    return cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
